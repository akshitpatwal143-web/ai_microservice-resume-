from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict
from google import genai
import os
import json
import re
import httpx
from datetime import datetime

app = FastAPI()

# -----------------------------
# Initialize Gemini Client
# -----------------------------
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set in environment.")

client = genai.Client(api_key=api_key)

# -----------------------------
# Request Model
# -----------------------------
class ResumeRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None

# -----------------------------
# Response Models
# -----------------------------
class TrendAnalysis(BaseModel):
    field: str
    current_trends: List[str]
    hot_skills: List[str]
    market_demand: str
    percentile_ranking: int

class JobOpportunity(BaseModel):
    title: str
    company: str
    url: str
    relevance_score: int

class ChainOfThought(BaseModel):
    step: str
    reasoning: str
    findings: str

class EnhancedResumeAnalysis(BaseModel):
    skills: List[str]
    missing_skills: List[str]
    score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: str
    chain_of_thought: List[ChainOfThought]
    trend_analysis: TrendAnalysis
    job_opportunities: List[JobOpportunity]

# -----------------------------
# Helper Functions
# -----------------------------
async def fetch_job_opportunities(skills: List[str], field: str) -> List[JobOpportunity]:
    """
    Fetch relevant job opportunities using Adzuna API
    You can also use: The Muse API, GitHub Jobs, or other job APIs
    """
    opportunities = []
    
    try:
        # Using Adzuna API (free tier available)
        # Sign up at: https://developer.adzuna.com/
        adzuna_app_id = os.getenv("ADZUNA_APP_ID", "")
        adzuna_app_key = os.getenv("ADZUNA_APP_KEY", "")
        
        if adzuna_app_id and adzuna_app_key:
            # Search for jobs based on top skills
            search_term = " ".join(skills[:3])  # Use top 3 skills
            
            async with httpx.AsyncClient() as http_client:
                url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
                params = {
                    "app_id": adzuna_app_id,
                    "app_key": adzuna_app_key,
                    "what": search_term,
                    "results_per_page": 5,
                    "content-type": "application/json"
                }
                
                response = await http_client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    for job in data.get("results", [])[:5]:
                        opportunities.append(JobOpportunity(
                            title=job.get("title", "N/A"),
                            company=job.get("company", {}).get("display_name", "N/A"),
                            url=job.get("redirect_url", "#"),
                            relevance_score=85  # You can calculate this based on skill match
                        ))
        
        # Fallback: Generate Google Jobs search links if API not available
        if not opportunities:
            for skill in skills[:3]:
                opportunities.append(JobOpportunity(
                    title=f"{skill} Positions",
                    company="Multiple Companies",
                    url=f"https://www.google.com/search?q={skill.replace(' ', '+')}+jobs",
                    relevance_score=70
                ))
    
    except Exception as e:
        print(f"Error fetching job opportunities: {e}")
        # Provide fallback search links
        opportunities.append(JobOpportunity(
            title=f"{field} Opportunities",
            company="Multiple Companies",
            url=f"https://www.linkedin.com/jobs/search/?keywords={field.replace(' ', '%20')}",
            relevance_score=60
        ))
    
    return opportunities[:5]  # Return top 5

# -----------------------------
# AI Resume Analyzer with Enhanced Features
# -----------------------------
@app.post("/ai/analyze", response_model=EnhancedResumeAnalysis)
async def analyze_resume(data: ResumeRequest):
    """
    Enhanced resume analysis with:
    - Chain of thought reasoning
    - Industry trend analysis
    - Percentile ranking
    - Job opportunities
    """
    
    # Basic validation
    if len(data.resume_text.strip()) < 50:
        return EnhancedResumeAnalysis(
            skills=[],
            missing_skills=[],
            score=0,
            strengths=[],
            weaknesses=[],
            suggestions="Resume content too short to analyze.",
            chain_of_thought=[],
            trend_analysis=TrendAnalysis(
                field="Unknown",
                current_trends=[],
                hot_skills=[],
                market_demand="Low",
                percentile_ranking=0
            ),
            job_opportunities=[]
        )
    
    # -----------------------------
    # Step 1: Initial Analysis with Chain of Thought
    # -----------------------------
    analysis_prompt = f"""
You are an expert ATS Resume Evaluation System with deep knowledge of current industry trends.

RESUME:
{data.resume_text}

{"JOB DESCRIPTION:\n" + data.job_description if data.job_description else ""}

Analyze this resume using CHAIN OF THOUGHT reasoning. Think step-by-step:

1. IDENTIFY THE FIELD: What industry/field is this resume for?
2. EXTRACT SKILLS: What technical and soft skills are present?
3. ASSESS EXPERIENCE: How does the experience align with current market expectations?
4. IDENTIFY GAPS: What critical skills or experiences are missing for {datetime.now().year}?
5. CALCULATE SCORE: Based on modern ATS standards and industry requirements

Return response in this EXACT JSON format:
{{
  "skills": ["skill1", "skill2"],
  "missing_skills": ["missing1", "missing2"],
  "score": 75,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "suggestions": "detailed suggestions",
  "field": "Software Engineering",
  "chain_of_thought": [
    {{"step": "Field Identification", "reasoning": "...", "findings": "..."}},
    {{"step": "Skills Extraction", "reasoning": "...", "findings": "..."}},
    {{"step": "Experience Assessment", "reasoning": "...", "findings": "..."}},
    {{"step": "Gap Analysis", "reasoning": "...", "findings": "..."}},
    {{"step": "Scoring", "reasoning": "...", "findings": "..."}}
  ]
}}

IMPORTANT:
- Be specific and detailed in your reasoning
- Consider current {datetime.now().year} industry standards
- Score must be 0-100
- Return ONLY valid JSON, no markdown
"""
    
    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            contents=analysis_prompt
        )
        ai_output = response.text
        cleaned_output = re.sub(r"```json|```", "", ai_output).strip()
        
        try:
            initial_analysis = json.loads(cleaned_output)
        except json.JSONDecodeError:
            return {
                "error": "AI did not return valid JSON for initial analysis",
                "raw_output": ai_output
            }
        
        # Extract field for trend analysis
        field = initial_analysis.get("field", "Technology")
        
        # -----------------------------
        # Step 2: Industry Trend Analysis & Percentile Ranking
        # -----------------------------
        trend_prompt = f"""
You are an industry trends expert analyzing the {field} field as of {datetime.now().year}.

Based on this candidate's profile:
- Skills: {', '.join(initial_analysis.get('skills', []))}
- Experience Level: (inferred from resume)

Provide a comprehensive trend analysis:

Return EXACT JSON:
{{
  "current_trends": ["trend1", "trend2", "trend3"],
  "hot_skills": ["skill1", "skill2", "skill3"],
  "market_demand": "High/Medium/Low",
  "percentile_ranking": 65,
  "ranking_explanation": "This candidate ranks in the 65th percentile because..."
}}

Consider:
- Current {datetime.now().year} job market trends in {field}
- Emerging technologies and methodologies
- In-demand skills vs. candidate's skillset
- Industry standards for experience level

Percentile Ranking Guidelines:
- 90-100: Top tier, highly competitive, matches latest trends
- 70-89: Strong candidate, most modern skills present
- 50-69: Average, has core skills but missing some modern trends
- 30-49: Below average, significant skill gaps
- 0-29: Needs major improvement, outdated skillset

Return ONLY valid JSON.
"""
        
        trend_response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=trend_prompt
        )
        trend_output = re.sub(r"```json|```", "", trend_response.text).strip()
        
        try:
            trend_data = json.loads(trend_output)
        except json.JSONDecodeError:
            trend_data = {
                "current_trends": ["AI/ML Integration", "Cloud Technologies", "Automation"],
                "hot_skills": ["Python", "Cloud Platforms", "Data Analysis"],
                "market_demand": "High",
                "percentile_ranking": 50,
                "ranking_explanation": "Analysis unavailable"
            }
        
        # -----------------------------
        # Step 3: Fetch Job Opportunities
        # -----------------------------
        job_opportunities = await fetch_job_opportunities(
            initial_analysis.get("skills", []),
            field
        )
        
        # -----------------------------
        # Step 4: Compile Final Response
        # -----------------------------
        return EnhancedResumeAnalysis(
            skills=initial_analysis.get("skills", []),
            missing_skills=initial_analysis.get("missing_skills", []),
            score=initial_analysis.get("score", 0),
            strengths=initial_analysis.get("strengths", []),
            weaknesses=initial_analysis.get("weaknesses", []),
            suggestions=initial_analysis.get("suggestions", ""),
            chain_of_thought=[
                ChainOfThought(**cot) 
                for cot in initial_analysis.get("chain_of_thought", [])
            ],
            trend_analysis=TrendAnalysis(
                field=field,
                current_trends=trend_data.get("current_trends", []),
                hot_skills=trend_data.get("hot_skills", []),
                market_demand=trend_data.get("market_demand", "Medium"),
                percentile_ranking=trend_data.get("percentile_ranking", 50)
            ),
            job_opportunities=job_opportunities
        )
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "An error occurred during analysis"
        }

# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/")
def read_root():
    return {
        "service": "Enhanced AI Resume Analyzer",
        "version": "2.0",
        "features": [
            "Chain of Thought Analysis",
            "Industry Trend Analysis",
            "Percentile Ranking",
            "Job Opportunity Matching"
        ]
    }

# -----------------------------
# Run with: uvicorn enhanced_resume_analyzer:app --reload
# -----------------------------
