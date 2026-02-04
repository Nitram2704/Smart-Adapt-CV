from jinja2 import Environment, FileSystemLoader
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception as e:
    print(f"Warning: WeasyPrint could not be loaded. PDF generation will be disabled. Error: {e}")
    WEASYPRINT_AVAILABLE = False
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render_cv_html(data: dict) -> str:
    """Renders the CV data into HTML using Jinja2."""
    template = env.get_template("cv_template.html")
    return template.render(**data)

def generate_pdf(html_content: str, output_path: str):
    """Converts HTML content to a PDF file using WeasyPrint."""
    if not WEASYPRINT_AVAILABLE:
        raise ImportError("WeasyPrint is not available. Please install GTK+ libraries as per WeasyPrint documentation.")
    HTML(string=html_content).write_pdf(output_path)
