import os
import json
import sys
# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.parser import extract_text_from_pdf, parse_text_to_master_profile
from core.ai_engine import AIEngine, OpenRouterProvider, FallbackProvider
from core.generator import render_cv_html, generate_pdf
from dotenv import load_dotenv

load_dotenv()

# Initialize AI for parsing
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("ERROR: OPENROUTER_API_KEY not found.")
    sys.exit(1)

provider = OpenRouterProvider(api_key=api_key)
# Hack: Pass provider directly as it matches the 'generate' interface expected by parser
profile = None

INPUT_PDF = os.path.join(os.path.dirname(__file__), "inputs", "cv_pjjr_Martin_Sanchez_Urrego.pdf")
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "outputs", "extracted_profile.json")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "outputs", "cv_synced_content.pdf")

def main():
    print(f"--- Extracting Content from {INPUT_PDF} ---")
    
    if not os.path.exists(INPUT_PDF):
        print(f"ERROR: Input file not found: {INPUT_PDF}")
        return

    # 1. Extract Text
    text = extract_text_from_pdf(INPUT_PDF)
    print(f"Extracted {len(text)} chars.")

    # 2. Parse to JSON
    print("Parsing with AI...")
    profile = parse_text_to_master_profile(text, provider)
    
    # 3. Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    print(f"Saved profile to {OUTPUT_JSON}")

    # 4. Generate PDF with this profile
    print("Generating Preview PDF...")
    
    # Ensure 'language' key exists for template
    profile["language"] = "es" 
    
    # Render HTML
    html = render_cv_html(profile)
    
    # Generate PDF
    generate_pdf(html, OUTPUT_PDF)
    print(f"SUCCESS: Generated {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
