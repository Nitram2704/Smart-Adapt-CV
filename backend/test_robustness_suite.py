import os
import sys
import json
import unittest
from dotenv import load_dotenv

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from core.ai_engine import AIEngine, LLMProvider
from core.generator import render_cv_html

class MockEmptyProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        # Simulate AI returning mostly empty JSON
        return json.dumps({
            "basic_info": {"name": "Test User"},
            "summary": "Short summary"
        })

class MockMalformedProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        # Simulate AI returning text with JSON inside
        return "Sure! Here is your CV: " + json.dumps({
            "basic_info": {"name": "Test User"},
            "skills": {"product": ["Testing"]}
        }) + " Hope this helps!"

class TestCVRobustness(unittest.TestCase):
    def setUp(self):
        self.master_profile = {
            "basic_info": {"name": "Martin", "email": "m@m.com"},
            "languages": []
        }
        self.analysis = {"detected_language": "en"}

    def test_missing_keys_recovery(self):
        """Test that AI missing keys don't break the profile structure."""
        engine = AIEngine(MockEmptyProvider())
        result = engine.generate_optimized_content(self.master_profile, self.analysis, [])
        
        self.assertIn("experience", result)
        self.assertIsInstance(result["experience"], list)
        self.assertIn("project_management", result["skills"])

    def test_malformed_json_recovery(self):
        """Test that JSON wrapped in text is correctly extracted."""
        engine = AIEngine(MockMalformedProvider())
        result = engine.generate_optimized_content(self.master_profile, self.analysis, [])
        
        self.assertEqual(result["basic_info"]["name"], "Test User")
        # Test schema synchronization
        self.assertIn("project_management", result["skills"])
        self.assertNotIn("product", result["skills"])

    def test_render_consistency(self):
        """Test that the rendered HTML contains basic section markers even with empty data."""
        data = {
            "basic_info": {"name": "Martin"},
            "summary": "Test",
            "skills": {"project_management": []},
            "experience": [],
            "education": [],
            "languages": [],
            "language": "en"
        }
        html = render_cv_html(data)
        self.assertIn("Professional summary", html)
        self.assertIn("PROJECT EXPERIENCE", html)

if __name__ == "__main__":
    unittest.main()
