from jinja2 import Environment, FileSystemLoader
import re
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception as e:
    print(f"Warning: WeasyPrint could not be loaded. PDF generation will be disabled. Error: {e}")
    WEASYPRINT_AVAILABLE = False
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def markdown_to_html(text):
    """Simple markdown-to-html converter for bold and italic."""
    if not isinstance(text, str):
        return text
    # Convert bold **text** or __text__ to <strong>text</strong>
    text = re.sub(r'(\*\*|__)(.*?)\1', r'<strong>\2</strong>', text)
    # Convert italic *text* or _text_ to <em>text</em>
    text = re.sub(r'(\*|_)(.*?)\1', r'<em>\2</em>', text)
    return text

# Register the filter
env.filters['md'] = markdown_to_html

def render_cv_html(data: dict, template_name: str = "cv_template.html") -> str:
    """Renders the CV data into HTML using Jinja2."""
    print(f"DEBUG: Rendering CV with template {template_name} and keys: {list(data.keys())}")
    template = env.get_template(template_name)
    return template.render(**data)

def render_cover_letter_html(data: dict) -> str:
    """Renders the Cover Letter data into HTML using Jinja2."""
    template = env.get_template("cover_letter_template.html")
    return template.render(**data)

def generate_pdf(html_content: str, output_path: str):
    """Converts HTML content to a PDF file using WeasyPrint."""
    if not WEASYPRINT_AVAILABLE:
        raise ImportError("WeasyPrint is not available. Please install GTK+ libraries as per WeasyPrint documentation.")
    HTML(string=html_content).write_pdf(output_path)
