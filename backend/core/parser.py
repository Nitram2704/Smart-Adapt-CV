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
    return text

def parse_text_to_master_profile(text: str, ai_client) -> Dict:
    """
    Uses the provided AI client to parse raw text into a Master Profile JSON.
    """
    system_prompt = "You are an expert AI CV Parser and ATS researcher. Your goal is to extract structured data from raw CV text with 100% accuracy, specifically focusing on identifying personal and professional projects."
    prompt = f"""
    Analyze the following CV text and extract it into a STRICT JSON format.
    
    PREFERRED CONTACT INFO (Use these if found or mentioned):
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
        "product": [] 
      }},
      "experience": [
        {{ "company": "...", "role": "...", "duration": "...", "highlights": ["bullet points..."], "stack": ["tech used..."] }}
      ],
      "projects": [
        {{ "name": "Project Name", "description": "What was built...", "impact_metrics": "Results or technical scale..." }}
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
        print(f"Failed to parse CV JSON: {e}")
        print(f"Raw Response: {response_text}")
        
        if "ERROR_QUOTA_EXCEEDED" in response_text or "ERROR_ALL_PROVIDERS_FAILED" in response_text:
            error_msg = "Quota Hit (Auto-Switching...)"
            summary_msg = f"Gemini API quota reached. {response_text}. Attempting fallback..."
            if "Local Ollama Success" in response_text: # This won't be here since it returns the JSON, but just in case
                error_msg = "Extracted via Local AI"
            summary_msg = "Your Gemini API limit has been reached. Please wait 60 seconds or use a local model if available."
            
        return {
            "basic_info": {"name": error_msg, "email": ""},
            "summary": summary_msg,
            "skills": {"languages": [], "frameworks": [], "tools": []},
            "experience": [],
            "projects": []
        }
