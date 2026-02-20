import os
import sys
from dotenv import load_dotenv

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from core.generator import render_cv_html

# Absolutely no data
data = {}

print("--- Testing HTML Rendering with NO Data ---")
try:
    html = render_cv_html(data)
    # Check if main sections are present in HTML
    sections = ["EDUCACIÓN", "HERRAMIENTAS", "Perfil profesional", "REFERENCIAS"]
    for section in sections:
        if section in html:
            print(f"Section '{section}' found in HTML.")
        else:
            print(f"Section '{section}' NOT found in HTML.")
except Exception as e:
    print(f"FAILED to render: {e}")
