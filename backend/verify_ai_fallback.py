
import sys
import os
import json
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ai_engine import AIEngine, LLMProvider

class GarbageProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        return "I am not a JSON robot. Beep boop."

class EmptyJsonProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        return "{}"

class PartialJsonProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        return '{"basic_info": {"name": "AI Name"}, "skills": {}}'

def test_fallback_mechanism():
    print("\n--- Testing AI Engine Fallback Mechanism ---")
    
    # Setup Master Profile
    master_profile = {
        "basic_info": {"name": "Master Name", "email": "master@example.com"},
        "summary": "Master Summary",
        "skills": {"backend": ["Python"], "frontend": []},
        "experience": [{"company": "Master Corp", "role": "Dev", "highlights": ["Did stuff"]}],
        "education": [{"institution": "Master Univ", "degree": "BS"}],
        "languages": [{"language": "English", "level": "Native"}],
        "certifications": []
    }
    
    analysis = {"detected_language": "en"}
    portfolio = {}

    # 1. Test Garbage Response
    print("\nTest 1: Garbage Response from AI (Should trigger error and return Master Profile with just 'language') but wait...")
    # My logic:
    # try: load json. FAIL. except: returns {}
    # Then merge check loop.
    # summary is missing -> master summary.
    # skills missing -> master skills.
    # So effectively, it returns merge of empty + Master.
    
    provider = GarbageProvider()
    engine = AIEngine(provider)
    result = engine.generate_optimized_content(master_profile.copy(), analysis, portfolio)
    
    print(f"Result keys: {list(result.keys())}")
    if result.get("summary") == "Master Summary":
        print("PASS: Fallback to Master Summary successful.")
    else:
        print(f"FAIL: Expected Master Summary but got '{result.get('summary')}'")
        
    if len(result.get("experience", [])) > 0:
         print("PASS: Fallback to Master Experience successful.")
    else:
         print(f"FAIL: Expected Master Corp, got {result.get('experience')}")


    # 2. Test Partial JSON Response
    print("\nTest 2: Partial JSON Response from AI (Merging)")
    # AI returns: {"basic_info": {"name": "AI Name"}, "skills": {}}
    # skills is empty dict -> merge with Master skills.
    # summary is missing -> merge with Master summary.
    
    provider = PartialJsonProvider()
    engine = AIEngine(provider)
    result = engine.generate_optimized_content(master_profile.copy(), analysis, portfolio)
    
    print(f"Result keys: {list(result.keys())}")
    
    if result.get("basic_info", {}).get("name") == "AI Name":
        print("PASS: AI Data (basic_info.name) preserved.")
    else:
        print(f"FAIL: Expected 'AI Name', got '{result.get('basic_info', {}).get('name')}'")
        
    if "backend" in result.get("skills", {}):
        print("PASS: Fallback for empty AI skills successful.")
    else:
        print(f"FAIL: Skills fallback failed. Got {result.get('skills')}")

    if result.get("summary") == "Master Summary":
        print("PASS: Fallback for missing AI summary successful.")
    else:
        print(f"FAIL: Missing summary fallback failed.")

if __name__ == "__main__":
    test_fallback_mechanism()
