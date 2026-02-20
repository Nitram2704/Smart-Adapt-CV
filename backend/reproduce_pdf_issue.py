
import os
import sys
# Add the current directory to sys.path so we can import from core
sys.path.append(os.path.join(os.path.dirname(__file__)))

from core.generator import render_cv_html, generate_pdf

def test_pdf_generation():
    dummy_data = {
        "language": "en",
        "basic_info": {
            "name": "John Doe",
            "title": "Senior Software Engineer",
            "phone": "+1 234 567 890",
            "email": "john.doe@example.com",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "github_url": "https://github.com/johndoe",
            "portfolio_url": "https://johndoe.com"
        },
        "summary": "Experienced software engineer with a passion for building scalable web applications.",
        "skills": {
            "backend": ["Python", "Django", "FastAPI"],
            "frontend": ["React", "TypeScript", "Tailwind CSS"],
            "databases": ["PostgreSQL", "Redis"],
            "cloud": ["AWS", "Docker"],
            "architecture": ["Microservices", "REST"],
            "project_management": ["JIRA", "Agile"]
        },
        "experience": [
            {
                "role": "Software Engineer",
                "company": "Tech Corp",
                "duration": "2020 - Present",
                "highlights": ["Built a thing", "Optimized another thing"]
            },
            {
                "role": "Junior Developer",
                "company": "Startup Inc",
                "duration": "2018 - 2020",
                "highlights": ["Fixed bugs", "Implemented features"]
            }
        ],
        "education": [
            {
                "degree": "B.Sc. Computer Science",
                "institution": "University of Technology",
                "year": "2018"
            }
        ],
        "certifications": [
            {
                "name": "AWS Certified Solutions Architect",
                "issuer": "Amazon Web Services",
                "year": "2021"
            }
        ],
        "languages": [
            {"language": "English", "level": "Native"},
            {"language": "Spanish", "level": "Intermediate"}
        ]
    }

    output_html = "test_cv.html"
    output_pdf = "test_cv.pdf"

    print("Rendering HTML...")
    html_content = render_cv_html(dummy_data)
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML saved to {output_html}")
    
    print("Generating PDF...")
    generate_pdf(html_content, output_pdf)
    print(f"PDF saved to {output_pdf}")

if __name__ == "__main__":
    test_pdf_generation()
