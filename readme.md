# AI Resume Analyzer - GenAI Microservice

## Overview
This is the AI microservice responsible for analyzing resumes using Google Gemini.

## Tech Stack
- Python 3.11
- FastAPI
- Google Gemini (2.5 Flash)

## API Endpoint

POST /ai/analyze

Request:
{
  "resume_text": "string",
  "job_description": "string (optional)"
}

Response:
{
  "skills": [],
  "missing_skills": [],
  "score": number,
  "strengths": [],
  "weaknesses": [],
  "suggestions": ""
}

## Setup

1. Create virtual environment
2. Install requirements:
   pip install -r requirements.txt
3. Set environment variable:
   export GOOGLE_API_KEY=your_key
4. Run:
   uvicorn ai_service:app --reload
