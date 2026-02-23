import fitz
import sys

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    path = "C:/Users/marti/Desktop/CV/Software Engineer Intern.pdf"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    print(extract_text(path))
