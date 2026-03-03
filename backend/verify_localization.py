import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.generator import render_cv_html
from core.locales import get_labels

def test_localization():
    # Mock data
    mock_profile = {
        "basic_info": {"name": "Test User", "email": "test@example.com", "phone": "123456"},
        "summary": "Esto es un resumen en español.",
        "education": [{"institution": "UdeA", "year": "2020", "degree": "Ingeniero"}],
        "experience": [{"company": "Empresa X", "role": "Developer", "duration": "2 años", "highlights": ["Logro 1"]}],
        "skills": {"backend": ["Python", "Docker"]},
        "certifications": [{"name": "Cert 1", "issuer": "Org", "year": "2021"}],
        "languages": [{"language": "Español", "level": "Nativo"}],
        "language": "es" # Spanish detected
    }
    
    # 1. Get labels
    mock_profile["labels"] = get_labels(mock_profile["language"])
    
    # 2. Render ATS template
    html_es = render_cv_html(mock_profile, template_name="ats_foreign_template.html")
    
    # 3. Check for Spanish titles
    required_spanish = ["Resumen Profesional", "Educación", "Experiencia", "Habilidades", "Certificaciones", "Idiomas"]
    print("Checking Spanish titles in ATS template:")
    for title in required_spanish:
        if title in html_es:
            print(f"  [PASS] Found: {title}")
        else:
            print(f"  [FAIL] Missing: {title}")
            
    # Test English
    mock_profile["language"] = "en"
    mock_profile["labels"] = get_labels("en")
    html_en = render_cv_html(mock_profile, template_name="ats_foreign_template.html")
    
    required_english = ["Professional Summary", "Education", "Experience", "Skills", "Certifications", "Languages"]
    print("\nChecking English titles in ATS template:")
    for title in required_english:
        if title in html_en:
            print(f"  [PASS] Found: {title}")
        else:
            print(f"  [FAIL] Missing: {title}")

if __name__ == "__main__":
    test_localization()
