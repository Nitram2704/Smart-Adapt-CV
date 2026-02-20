import sys
import os
from weasyprint import HTML, CSS

# Path to the debug HTML file verification
DEBUG_HTML_PATH = os.path.join(os.path.dirname(__file__), "outputs", "cv_debug_MARTIN_SANCHEZ_URREGO.html")
OUTPUT_PDF_PATH = os.path.join(os.path.dirname(__file__), "outputs", "test_render.pdf")

def test_render():
    print(f"--- Testing PDF Rendering ---")
    
    if not os.path.exists(DEBUG_HTML_PATH):
        print(f"ERROR: Debug HTML file not found at {DEBUG_HTML_PATH}")
        return

    try:
        print(f"Reading HTML from: {DEBUG_HTML_PATH}")
        with open(DEBUG_HTML_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        print(f"HTML Content Length: {len(html_content)} bytes")
        
        # Test 1: Simple Render
        print("Attempting validation render...")
        HTML(string=html_content).write_pdf(OUTPUT_PDF_PATH)
        print(f"SUCCESS: PDF written to {OUTPUT_PDF_PATH}")
        
    except Exception as e:
        print(f"CRITICAL ERROR during rendering: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_render()
