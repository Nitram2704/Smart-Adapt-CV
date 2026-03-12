import json
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from core.ai_engine import AIEngine, GeminiProvider, FallbackProvider
from core.portfolio import load_portfolio_projects
from dotenv import load_dotenv

load_dotenv()

def test_date_stipulation():
    # Mock analysis with seniority
    analysis = {
        "detected_language": "es",
        "job_role": "Senior Fullstack Developer",
        "match_score": 85,
        "seniority_detected": "Senior (5+ years)",
        "relevant_projects": [
            {"id": "smart_adapt_cv", "name": "Smart-Adapt CV"},
            {"id": "finanzas_personales", "name": "Finanzas Personales"},
            {"id": "pos_system", "name": "POS System"}
        ]
    }

    # Mock master profile
    master_profile = {
        "basic_info": {"name": "Test User", "title": "Developer"},
        "experience": []
    }

    portfolio_projects = load_portfolio_projects()
    
    # Initialize Engine (Need at least one provider)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found. Skipping verification.")
        return

    engine = AIEngine(GeminiProvider(api_key=api_key))
    
    print("Generating optimized content for SENIOR role...")
    optimized = engine.generate_optimized_content(master_profile, analysis, portfolio_projects)
    
    print("\n--- RESULTS ---")
    for exp in optimized.get("experience", []):
        print(f"Project: {exp.get('company')} | Role: {exp.get('role')} | Duration: {exp.get('duration')}")
    
    # Check if dates are present and logical (manual check from output)
    # The expected output should show dates like "2024 - Present", "2023", etc.

if __name__ == "__main__":
    test_date_stipulation()
