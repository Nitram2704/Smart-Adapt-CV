import fitz
import os

pdf_path = "C:/Users/marti/Desktop/CV/cv_pjjr_Martin_Sanchez_Urrego.pdf"

if os.path.exists(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print(f"Extracted {len(text)} characters.")
    print("Preview of first 200 chars:")
    print(text[:200])
else:
    print(f"File not found: {pdf_path}")
