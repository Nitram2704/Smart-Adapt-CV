import fitz
import sys

def check_pages(path):
    try:
        doc = fitz.open(path)
        print(f"PAGE_COUNT:{doc.page_count}")
        doc.close()
    except Exception as e:
        print(f"ERROR:{e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_pages(sys.argv[1])
    else:
        print("Usage: python check_pages.py <pdf_path>")
