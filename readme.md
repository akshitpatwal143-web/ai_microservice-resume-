# Enhanced AI Resume Analyzer 🚀

An intelligent FastAPI-based resume analysis system powered by Google's Gemini AI that provides:
- **Chain of Thought** reasoning for transparent analysis
- **Industry Trend Analysis** with current market insights
- **Percentile Ranking** to show where candidates stand
- **Job Opportunities** matching the candidate's skillset

## ✨ New Features

### 1. Chain of Thought Analysis
The AI now shows its reasoning process step-by-step:
- Field identification
- Skills extraction
- Experience assessment
- Gap analysis
- Score calculation

### 2. Industry Trend Analysis
Get insights on:
- Current trends in the candidate's field (2025)
- Hot skills in demand
- Market demand level
- Percentile ranking (where the resume stands compared to others)

### 3. Job Opportunities
Automatic job matching with:
- Relevant job listings based on skills
- Company names and links
- Relevance scores

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key ([Get it here](https://ai.google.dev/))
- (Optional) Adzuna API credentials for enhanced job search ([Sign up](https://developer.adzuna.com/))

## 🔧 Installation

1. **Clone or download the files**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Your `.env` file should look like:
```
GOOGLE_API_KEY=your_actual_gemini_key
ADZUNA_APP_ID=your_adzuna_id  # Optional
ADZUNA_APP_KEY=your_adzuna_key  # Optional
```

## 🚀 Running the Application

```bash
uvicorn enhanced_resume_analyzer:app --reload
```

The API will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## 📡 API Usage

### Endpoint: `POST /ai/analyze`

**Request Body:**
```json
{
  "resume_text": "John Doe\nSoftware Engineer with 5 years experience...",
  "job_description": "Looking for a senior developer with Python, React..." // Optional
}
```

**Response:**
```json
{
  "skills": ["Python", "React", "Docker", "AWS"],
  "missing_skills": ["Kubernetes", "TypeScript"],
  "score": 78,
  "strengths": [
    "Strong backend development experience",
    "Cloud infrastructure knowledge"
  ],
  "weaknesses": [
    "Limited frontend framework experience",
    "No DevOps certifications"
  ],
  "suggestions": "Consider learning Kubernetes and obtaining AWS certification...",
  
  "chain_of_thought": [
    {
      "step": "Field Identification",
      "reasoning": "Based on keywords like 'Software Engineer', 'Python', 'API development'",
      "findings": "Candidate is in Software Development/Engineering field"
    },
    {
      "step": "Skills Extraction",
      "reasoning": "Identified both technical and soft skills from resume",
      "findings": "Found 12 technical skills and 5 soft skills"
    }
    // ... more steps
  ],
  
  "trend_analysis": {
    "field": "Software Engineering",
    "current_trends": [
      "AI/ML Integration in applications",
      "Microservices architecture",
      "Cloud-native development"
    ],
    "hot_skills": [
      "Kubernetes",
      "TypeScript",
      "GraphQL",
      "Terraform"
    ],
    "market_demand": "High",
    "percentile_ranking": 72
  },
  
  "job_opportunities": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "url": "https://example.com/job/123",
      "relevance_score": 85
    }
    // ... more opportunities
  ]
}
```

## 🧪 Testing with cURL

```bash
curl -X POST "http://localhost:8000/ai/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Jane Smith\nData Scientist with 3 years of experience in Python, Machine Learning, and statistical analysis. Built predictive models using scikit-learn and TensorFlow.",
    "job_description": "Seeking a Data Scientist with expertise in ML, Python, and cloud platforms."
  }'
```

## 🔍 Understanding the Response

### Score (0-100)
- **90-100**: Exceptional, highly competitive
- **70-89**: Strong candidate
- **50-69**: Average, competitive with improvements
- **30-49**: Below average, needs significant work
- **0-29**: Major improvements needed

### Percentile Ranking
Shows where the candidate stands compared to others in their field:
- **90-100th**: Top 10% - highly competitive
- **70-89th**: Strong candidate
- **50-69th**: Average
- **30-49th**: Below average
- **0-29th**: Needs major improvement

### Chain of Thought
See the AI's reasoning process, making the analysis transparent and trustworthy.

### Trend Analysis
- **Current Trends**: What's hot in the industry right now
- **Hot Skills**: Most in-demand skills for 2025
- **Market Demand**: Overall hiring demand in the field

## 🌐 Alternative Job APIs

If you want to use different job search APIs:

1. **The Muse API** (Free tier available)
   - https://www.themuse.com/developers/api/v2

2. **GitHub Jobs** (Free)
   - https://jobs.github.com/api

3. **Adzuna** (Used in this implementation)
   - https://developer.adzuna.com/

4. **JSearch (RapidAPI)** (Free tier)
   - https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

Modify the `fetch_job_opportunities()` function to integrate your preferred API.

## 📊 Example Use Cases

1. **Job Seekers**: Understand how your resume compares to current market standards
2. **Career Coaches**: Provide data-driven feedback to clients
3. **HR Teams**: Quickly assess candidate fit for positions
4. **Recruiters**: Identify skill gaps and training needs

## 🛠️ Customization

### Adjust Trend Analysis Criteria
Edit the `trend_prompt` in the code to focus on specific industries or roles.

### Add More Job Sources
Extend `fetch_job_opportunities()` to aggregate from multiple APIs.

### Modify Scoring Algorithm
Update the Gemini prompt to adjust scoring criteria based on your needs.

## 🐛 Troubleshooting

**Issue**: "GOOGLE_API_KEY not set in environment"
- Solution: Make sure your `.env` file exists and contains the API key

**Issue**: Job opportunities show Google search links instead of specific jobs
- Solution: Add Adzuna API credentials or integrate another job API

**Issue**: Invalid JSON response
- Solution: This usually happens with complex resumes. The code has fallback handling.

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add more job APIs
- Improve the trend analysis
- Add visualization features
- Enhance the scoring algorithm

## 📧 Support

For issues or questions, please open an issue on the repository.

---

**Built with ❤️ using FastAPI and Google Gemini AI**
