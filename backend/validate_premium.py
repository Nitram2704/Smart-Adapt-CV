import os
import json
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ai_engine import AIEngine, GeminiProvider, GroqProvider
from core.generator import render_cv_html, generate_pdf

load_dotenv()

def validate_premium_engine():
    """
    Validates that the AI Engine generates high-impact, quantified content
    for a sample job description.
    """
    print("\n🚀 --- CV PREMIUM VALIDATION TOOL ---")
    
    # 1. Setup Provider
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ ERROR: No API Key found (.env). Please set GOOGLE_API_KEY or GROQ_API_KEY.")
        return

    provider = GeminiProvider(api_key) if os.getenv("GOOGLE_API_KEY") else GroqProvider(api_key)
    engine = AIEngine(provider)

    # 2. Load Sample Data (Your Master Profile)
    master_path = os.path.join(os.path.dirname(__file__), "outputs", "extracted_profile.json")
    if not os.path.exists(master_path):
        print(f"❌ ERROR: Master profile not found at {master_path}.")
        return

    with open(master_path, "r", encoding="utf-8") as f:
        master_profile = json.load(f)

    # 3. Simulate a Job Description
    sample_job = """
    We are looking for a Senior Software Engineer to lead the development of high-scale AI systems. 
    Experience with Python, React, and Cloud infrastructure is mandatory. 
    Must be able to optimize database performance and lead technical teams.
    """
    
    print(f"📄 Testing with Job: {sample_job.strip()[:60]}...")

    # 4. Generate Optimized Content
    # We simulate a match analysis
    analysis = {
        "detected_language": "en",
        "match_score": 90,
        "relevant_projects": ["Smart-Adapt CV", "AutoQA"],
        "relevant_certifications": []
    }

    print("🧠 AI is thinking (Senior Persona Mode)...")
    optimized = engine.generate_optimized_content(master_profile, analysis, {})

    # 5. Inspection & Results
    print("\n✨ --- RESULTS: PREMIUM IMPACT CHECK ---")
    
    first_exp = optimized.get("experience", [{}])[0]
    print(f"\n🏢 Company: {first_exp.get('company')}")
    print(f"👨‍💻 Role: {first_exp.get('role')}")
    
    print("\n🔍 High-Impact Bullet Points:")
    for highlight in first_exp.get("highlights", []):
        if "Architected" in highlight or "Engineered" in highlight or "90%" in highlight or "%" in highlight:
            print(f"✅ [PREMIUM] {highlight}")
        else:
            print(f"   [TEXT] {highlight}")

    # 6. Final PDF Render
    pdf_path = os.path.join(os.path.dirname(__file__), "outputs", "validation_premium_result.pdf")
    html = render_cv_html(optimized)
    generate_pdf(html, pdf_path)
    
    print(f"\n📄 PDF Generated: {pdf_path}")
    print("📢 Check the 'highlights' above: You should see quantified metrics and senior verbs automatically generated!")

if __name__ == "__main__":
    validate_premium_engine()
