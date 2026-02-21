import os
import json
import sys
# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.generator import render_cv_html, generate_pdf

INPUT_JSON = os.path.join(os.path.dirname(__file__), "outputs", "extracted_profile.json")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "outputs", "cv_synced_content.pdf")

def main():
    print(f"--- Fast Render from {INPUT_JSON} ---")
    
    if not os.path.exists(INPUT_JSON):
        print(f"ERROR: No extracted profile found at {INPUT_JSON}")
        return

    # 1. Load JSON
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        profile = json.load(f)
    
    # Ensure language exists
    profile["language"] = "es"
    
    print(f"Loaded profile for: {profile.get('basic_info', {}).get('name')}")

    # 2. Render HTML
    print("Rendering HTML with updated template...")
    html = render_cv_html(profile)
    
    # 3. Generate PDF
    print(f"Generating PDF to {OUTPUT_PDF}...")
    generate_pdf(html, OUTPUT_PDF)
    print(f"SUCCESS: Generated {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
