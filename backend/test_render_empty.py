import os
import sys
from dotenv import load_dotenv

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from core.generator import render_cv_html

# Mock empty but structurally correct data
data = {
    "basic_info": {
        "name": "Martin Sanchez Urrego",
        "title": "Software Engineer",
        "email": "martin@example.com",
        "phone": "123456789"
    },
    "summary": "",
    "skills": {},
    "experience": [],
    "education": [],
    "languages": [],
    "language": "es"
}

print("--- Testing HTML Rendering with Empty Data ---")
html = render_cv_html(data)

# Check if main sections are present in HTML
sections = ["PERFIL PROFESIONAL", "EXPERIENCIA EN PROYECTOS", "EDUCACIÓN", "HERRAMIENTAS"]
for section in sections:
    if section in html:
        print(f"Section '{section}' found in HTML.")
    else:
        print(f"Section '{section}' NOT found in HTML.")

# Save to a temporary HTML file to check
with open("test_empty.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\nSaved to test_empty.html")
