from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from google import genai
import os
import json
import re

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
# AI Resume Analyzer Endpoint
# -----------------------------
@app.post("/ai/analyze")
def analyze_resume(data: ResumeRequest):

    # Basic validation
    if len(data.resume_text.strip()) < 50:
        return {
            "skills": [],
            "missing_skills": [],
            "score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": "Resume content too short to analyze."
        }

    # Build prompt
    prompt = f"""
You are an ATS Resume Evaluation System.

Analyze the following resume carefully.

Resume:
{data.resume_text}

"""

    if data.job_description:
        prompt += f"""
Also compare it against this Job Description:
{data.job_description}
"""

    prompt += """

Return STRICT JSON in this exact format:

{
  "skills": [],
  "missing_skills": [],
  "score": number,
  "strengths": [],
  "weaknesses": [],
  "suggestions": ""
}

Rules:
- Score must be between 0 and 100.
- Only return JSON.
- No explanations.
- No markdown.
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=prompt
        )

        ai_output = response.text

        # -----------------------------
        # Clean Markdown if Present
        # -----------------------------
        cleaned_output = re.sub(r"```json|```", "", ai_output).strip()

        # -----------------------------
        # Parse JSON Safely
        # -----------------------------
        try:
            parsed_json = json.loads(cleaned_output)
            return parsed_json

        except json.JSONDecodeError:
            return {
                "error": "AI did not return valid JSON",
                "raw_output": ai_output
            }

    except Exception as e:
        return {
            "error": str(e)
        }
