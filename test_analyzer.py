"""
Test script for Enhanced Resume Analyzer
Run this after starting the server with: uvicorn enhanced_resume_analyzer:app --reload
"""

import requests
import json

# Sample resume text
SAMPLE_RESUME = """
Sarah Johnson
Data Scientist | Machine Learning Engineer

EXPERIENCE:
Senior Data Scientist at TechCorp (2021-Present)
- Built predictive models using Python, scikit-learn, and TensorFlow
- Developed ETL pipelines processing 10M+ records daily
- Implemented A/B testing frameworks
- Collaborated with product teams on feature prioritization

Data Analyst at StartupXYZ (2019-2021)
- Created dashboards using Tableau and Power BI
- Performed statistical analysis on user behavior data
- Automated reporting workflows with Python

SKILLS:
Programming: Python, SQL, R
ML/AI: TensorFlow, PyTorch, scikit-learn, XGBoost
Data: Pandas, NumPy, SQL, NoSQL
Visualization: Matplotlib, Seaborn, Tableau
Cloud: AWS (S3, EC2, SageMaker)

EDUCATION:
M.S. Computer Science - Stanford University (2019)
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Data Scientist - AI/ML Team

We're seeking an experienced Data Scientist to join our AI team.

Requirements:
- 3+ years in data science/ML roles
- Strong Python programming
- Experience with deep learning frameworks (TensorFlow/PyTorch)
- Kubernetes and Docker experience
- Cloud platform expertise (AWS/GCP/Azure)
- MLOps best practices
- Strong communication skills

Nice to have:
- LLM/NLP experience
- Scala or Java
- Airflow/Prefect
"""

def test_analyze_resume():
    """Test the enhanced resume analyzer"""
    
    url = "http://localhost:8000/ai/analyze"
    
    payload = {
        "resume_text": SAMPLE_RESUME,
        "job_description": SAMPLE_JOB_DESCRIPTION
    }
    
    print("🚀 Sending resume for analysis...\n")
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            print("="*60)
            print("📊 RESUME ANALYSIS RESULTS")
            print("="*60)
            
            # Basic Analysis
            print(f"\n🎯 Overall Score: {result['score']}/100")
            print(f"\n✅ Identified Skills ({len(result['skills'])}):")
            for skill in result['skills']:
                print(f"  • {skill}")
            
            print(f"\n❌ Missing Skills ({len(result['missing_skills'])}):")
            for skill in result['missing_skills']:
                print(f"  • {skill}")
            
            print(f"\n💪 Strengths:")
            for strength in result['strengths']:
                print(f"  • {strength}")
            
            print(f"\n⚠️  Weaknesses:")
            for weakness in result['weaknesses']:
                print(f"  • {weakness}")
            
            # Chain of Thought
            print("\n" + "="*60)
            print("🧠 CHAIN OF THOUGHT ANALYSIS")
            print("="*60)
            for cot in result['chain_of_thought']:
                print(f"\n📌 {cot['step']}")
                print(f"   Reasoning: {cot['reasoning']}")
                print(f"   Findings: {cot['findings']}")
            
            # Trend Analysis
            print("\n" + "="*60)
            print("📈 INDUSTRY TREND ANALYSIS")
            print("="*60)
            trend = result['trend_analysis']
            print(f"\n🏢 Field: {trend['field']}")
            print(f"📊 Market Demand: {trend['market_demand']}")
            print(f"🎖️  Percentile Ranking: {trend['percentile_ranking']}th percentile")
            
            print(f"\n🔥 Current Trends:")
            for trend_item in trend['current_trends']:
                print(f"  • {trend_item}")
            
            print(f"\n⭐ Hot Skills (In-Demand):")
            for skill in trend['hot_skills']:
                print(f"  • {skill}")
            
            # Job Opportunities
            print("\n" + "="*60)
            print("💼 JOB OPPORTUNITIES")
            print("="*60)
            for i, job in enumerate(result['job_opportunities'], 1):
                print(f"\n{i}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Relevance: {job['relevance_score']}%")
                print(f"   Link: {job['url']}")
            
            # Suggestions
            print("\n" + "="*60)
            print("💡 SUGGESTIONS FOR IMPROVEMENT")
            print("="*60)
            print(result['suggestions'])
            
            print("\n" + "="*60)
            print("✨ Analysis Complete!")
            print("="*60)
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the server is running with:")
        print("   uvicorn enhanced_resume_analyzer:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_analyze_resume()
