
import json
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from core.ai_engine import AIEngine
from core.locales import get_labels

class MockProvider:
    def generate(self, prompt, system_instruction=None):
        # Very simplified mock response for generation
        return json.dumps({
            "basic_info": {
                "name": "Martin Sanchez",
                "title": "Ingeniero de Software",
                "email": "martin@example.com",
                "phone": "+57 304 2621096"
            },
            "summary": "Ingeniero de Software experimentado...",
            "skills": {"backend": ["Python", "FastAPI"], "frontend": ["React"]},
            "experience": [
                {
                    "company": "PascualBet",
                    "role": "Fullstack Developer",
                    "duration": "Ago 2025 - Nov 2025",
                    "highlights": ["Sit: ...", "Task: ...", "Action: ...", "Result: ..."]
                }
            ],
            "certifications": [],
            "education": [],
            "languages": []
        })

def test_localization():
    print("Testing Localization Logic...")
    provider = MockProvider()
    engine = AIEngine(provider)
    
    master_profile = {
        "basic_info": {"name": "Martin", "title": "Software Engineer"}
    }
    
    # Test Spanish
    analysis_es = {"detected_language": "es", "relevant_projects": []}
    optimized_es = engine.generate_optimized_content(master_profile, analysis_es, {})
    
    print(f"Title in Spanish: {optimized_es.get('basic_info', {}).get('title')}")
    assert optimized_es['basic_info']['title'] == "Ingeniero de Software"
    print("✅ Localization Logic Passed")

def test_labels():
    print("Testing Labels...")
    labels_es = get_labels("es")
    assert labels_es['software_engineer'] == "Ingeniero de Software"
    assert labels_es['contact'] == "Contacto"
    print("✅ Labels Passed")

if __name__ == "__main__":
    test_localization()
    test_labels()
