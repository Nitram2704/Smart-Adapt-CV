import fitz  # PyMuPDF
import json
import re
from typing import Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print(f"DEBUG: Extracted {len(text)} characters from PDF.")
    # Debug cleanup
    print(f"DEBUG: Raw text length: {len(text)}")
    
    # The following lines are commented out as the functions 'extract_basic_info' and 'extract_experience_section' are not defined in the provided context.
    # If these functions are intended to be added, they must be defined elsewhere.
    # # 2. Extract sections using Regex
    # basic_info = extract_basic_info(text)
    # print(f"DEBUG: Parser extracted basic_info: {basic_info}")
    
    # experience = extract_experience_section(text)
    # print(f"DEBUG: Parser extracted experience entries: {len(experience)}")
    return text

def parse_text_to_master_profile(text: str, ai_client) -> Dict:
    """
    Uses the provided AI client to parse raw text into a Master Profile JSON.
    """
    system_prompt = "You are an expert AI CV Parser and ATS researcher. Your goal is to extract structured data from raw CV text with 100% accuracy, specifically focusing on identifying personal and professional projects."
    prompt = f"""
    Analyze the following CV text and extract it into a STRICT JSON format.
    
    PREFERRED CONTACT INFO (Use these if found or mentioned):
    - Phone: +57 304 2621096
    - GitHub: https://github.com/Nitram2704
    - LinkedIn: https://www.linkedin.com/in/martin-sanchez-urrego-3b14133a4/
    - Portfolio: https://nitram2704.github.io/CV/CV.html

    CRITICAL INSTRUCTION FOR PROJECTS:
    - Look for sections named 'EXPERIENCIA EN PROYECTOS', 'Projects', or 'Portfolio'.
    - IDENTIFY MAJOR PROJECTS: Each role in the user's CV typically corresponds to one major project (e.g., 'Mambo Fitness', 'PascualBet', 'Sistema Muelitas').
    - ONE PROJECT PER ROLE: Extract exactly ONE project entry per major role if it has a distinct project name. 
    - DO NOT split internal tasks (Architecture, Security, etc.) into separate projects; keep those as 'highlights' within the 'experience' section.
    - Result for 'projects' should typically contain ~3 items based on this CV.
    - Each project needs a 'name', 'description', and 'impact_metrics'.

    Structure:
    {{
      "basic_info": {{ 
        "name": "...", 
        "email": "...", 
        "phone": "...",
        "linkedin_url": "...", 
        "github_url": "...", 
        "portfolio_url": "...",
        "title": "Software Engineer" 
      }},
      "summary": "Professional summary...",
      "skills": {{ 
        "backend": [], 
        "frontend": [], 
        "databases": [], 
        "cloud": [], 
        "architecture": [], 
        "project_management": [] 
      }},
      "experience": [
        {{ "company": "...", "role": "...", "duration": "...", "highlights": ["bullet points..."], "stack": ["tech used..."] }}
      ],
      "projects": [
        {{ "name": "Project Name", "description": "What was built...", "impact_metrics": "Results or technical scale..." }}
      ],
      "certifications": [
        {{ "name": "...", "issuer": "...", "year": "..." }}
      ],
      "education": [
        {{ "institution": "...", "degree": "...", "year": "..." }}
      ],
      "languages": [
        {{ "language": "...", "level": "..." }}
      ]
    }}

    CV Text:
    {text}
    """
    
    response_text = ai_client.generate(prompt, system_prompt)
    try:
        # Robust extraction: find first '{' and last '}'
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            clean_json = response_text[start_idx:end_idx+1]
        else:
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            
        result = json.loads(clean_json)
        
        # Ensure base structure exists
        if "basic_info" not in result:
            result["basic_info"] = {"name": "Unknown", "email": ""}
        if "experience" not in result:
            result["experience"] = []
        if "projects" not in result:
            result["projects"] = []
            
        return result
    except Exception as e:
        import traceback
        print(f"CRITICAL ERROR in parse_text_to_master_profile: {type(e).__name__}: {e}")
        print(traceback.format_exc())
        print(f"Raw Response Snippet: {str(response_text)[:500]}")
        
        error_msg = "Error Parsing CV"
        summary_msg = "There was an error parsing your CV. Please ensure it's a valid PDF."
        
        if response_text:
            if "ERROR_QUOTA_EXCEEDED" in response_text or "QUOTA" in response_text.upper():
                error_msg = "Quota Hit (Auto-Switching...)"
                summary_msg = "API quota reached. Please wait 60 seconds or use a local model."
            elif "ERROR_ALL_PROVIDERS_FAILED" in response_text:
                error_msg = "Service Unavailable"
                summary_msg = "All AI providers failed. Check your internet or API keys."
            
        return {
            "basic_info": {"name": error_msg, "email": ""},
            "summary": summary_msg,
            "skills": {"backend": [], "frontend": [], "databases": [], "cloud": [], "architecture": [], "project_management": []},
            "experience": [],
            "projects": []
        }
