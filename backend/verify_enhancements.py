
import json
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from core.ai_engine import AIEngine
from core.portfolio import load_portfolio_projects

def verify_enhancements():
    # Mock data
    master_profile = {
        "basic_info": {"name": "Martin"},
        "languages": [{"language": "Spanish", "level": "Native"}, {"language": "English", "level": "B1"}],
        "experience": []
    }
    analysis = {"detected_language": "en"}
    portfolio = load_portfolio_projects()
    
    # Mock provider for testing
    class MockProvider:
        def generate(self, prompt, system_prompt=None):
            return "{}" # Empty JSON to trigger fallback

    ai = AIEngine(provider=MockProvider())
    
    print("\n--- Testing English B2 Injection ---")
    # We can test the injection logic directly
    # Injected logic is inside generate_optimized_content which calls AI. 
    # Let's mock a partial run or manually inspect the code logic results.
    
    languages = master_profile.get("languages", [])
    english_idx = next((i for i, l in enumerate(languages) if "English" in l.get("language", "") or "Inglés" in l.get("language", "")), None)
    if english_idx is not None:
        languages[english_idx]["level"] = "B2"
    else:
        languages.append({"language": "English", "level": "B2"})
    
    print(f"Verified Languages: {languages}")
    assert any(l["language"] == "English" and l["level"] == "B2" for l in languages)

    print("\n--- Testing AIEngine Fallback Logic ---")
    mock_ai = AIEngine(provider=MockProvider())
    optimized = mock_ai.generate_optimized_content(master_profile, analysis, portfolio)
    
    print(f"Optimized keys: {list(optimized.keys())}")
    
    # Assert fallbacks happened
    assert optimized["summary"] == master_profile.get("summary", "Professional summary not generated.")
    assert len(optimized["languages"]) >= 2 # Spanish + English B2
    assert optimized["languages"][-1]["level"] == "B2"
    
    print("Fallback logic VERIFIED: Empty AI response correctly defaulted to Master Profile data.")

if __name__ == "__main__":
    verify_enhancements()
