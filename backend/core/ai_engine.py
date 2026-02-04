import os
import json
import requests
import re
import google.generativeai as genai
from typing import Dict, Optional, Any, List
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        pass

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "glm4"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system_instruction:
            payload["system"] = system_instruction
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model_20 = genai.GenerativeModel('gemini-2.0-flash')
        self.model_15 = genai.GenerativeModel('gemini-1.5-flash')
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
        
        # 1. Try Gemini 2.0 Flash
        try:
            print("DEBUG: Attempting generation with gemini-2.0-flash...", flush=True)
            response = self.model_20.generate_content(full_prompt)
            print("DEBUG: Gemini 2.0 Success!", flush=True)
            return response.text
        except Exception as e:
            error_str = str(e)
            print(f"DEBUG: Gemini 2.0 Error: {error_str}", flush=True)
            
            if "429" in error_str or "ResourceExhausted" in error_str:
                # 2. Fallback to Gemini 1.5 Flash
                try:
                    print("DEBUG: 2.0 Quota exceeded. Falling back to gemini-1.5-flash...", flush=True)
                    response = self.model_15.generate_content(full_prompt)
                    print("DEBUG: Gemini 1.5 Success!", flush=True)
                    return response.text
                except Exception as e2:
                    error_str2 = str(e2)
                    print(f"DEBUG: Gemini 1.5 Fallback Error: {error_str2}", flush=True)
                    
                    # 3. Final Fallback to Ollama (Local)
                    try:
                        print(f"DEBUG: Gemini Quota totally exhausted. Falling back to Local Ollama ({self.ollama_model})...", flush=True)
                        import requests
                        response = requests.post(
                            "http://localhost:11434/api/generate",
                            json={
                                "model": self.ollama_model,
                                "prompt": full_prompt,
                                "stream": False
                            }
                        )
                        result = response.json()
                        print("DEBUG: Local Ollama Success!", flush=True)
                        return result.get("response", "")
                    except Exception as e3:
                        print(f"DEBUG: Local Ollama Fallback Error: {str(e3)}", flush=True)
                        return f"ERROR_ALL_PROVIDERS_FAILED_V4: {error_str2}. Local: {str(e3)}"
            
            return f"Error connecting to Gemini: {error_str}"

class AIEngine:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def analyze_cv_and_job(self, cv_json: Dict, job_text: str, portfolio_projects: List[Dict]) -> Dict:
        system_prompt = "You are an expert career coach and ATS optimization specialist."
        prompt = f"""
        Given the following CV data (JSON), a Job Vacancy description, and a list of available Portfolio Projects, perform a gap analysis.
        Identify:
        1. Match Score (0-100). Be highly realistic: if critical stack components are missing, the score should reflect that (don't default to 65%).
        2. Missing keywords or skills. Be specific about versions or specialized tools.
        3. Which 2-3 projects FROM THE PORTFOLIO LIST are most relevant to replace or augment existing projects.
        4. Recommendations for summary improvement.

        CV Data: {json.dumps(cv_json)}
        Job Vacancy: {job_text}
        Portfolio Projects: {json.dumps(portfolio_projects)}

        Return the result STRICTLY as a JSON object with the following structure:
        {{
          "match_score": 0-100,
          "missing_skills": ["skill1", "skill2"],
          "relevant_projects": [
            {{ "name": "Project Name", "reason": "Why it matches..." }}
          ],
          "recommendations": "Summary rewrite advice..."
        }}
        """
        response_text = self.provider.generate(prompt, system_prompt)
        try:
            # Robust extraction
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if json_match:
                clean_json = json_match.group(1)
            else:
                clean_json = response_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(clean_json)
            
            # Ensure all keys exist to prevent frontend crashes
            defaults = {
                "match_score": 0,
                "missing_skills": [],
                "relevant_projects": [],
                "recommendations": ""
            }
            for key, val in defaults.items():
                if key not in result or result[key] is None:
                    result[key] = val
            return result
        except:
            return {
                "error": "Failed to parse AI response as JSON", 
                "raw": response_text,
                "match_score": 0,
                "missing_skills": [],
                "relevant_projects": [],
                "recommendations": "Error parsing AI response."
            }

    def generate_optimized_content(self, master_profile: dict, analysis: dict, portfolio_projects: dict) -> dict:
        """
        Generates the final JSON for the CV, rewriting summary/experience based on analysis.
        Injects portfolio projects into the experience section.
        """
        system_prompt = "You are an expert CV Writer. Your goal is to maximize the candidate's match score by strategically rewriting their profile."
        
        prompt = f"""
        Master Profile: {json.dumps(master_profile)}
        Analysis Recommendations: {json.dumps(analysis)}
        Available Portfolio Projects: {json.dumps(portfolio_projects)}

        Based on the recommendations, generate a final optimized CV structure.
        
        CRITICAL INSTRUCTIONS:
        1. **LANGUAGE**: Detect the language of the 'Job Vacancy' from the analysis context (implied). All generated text MUST be in that language.
        2. **LANGUAGE FLAG**: Add a root-level key "language" with value "en" if English or "es" if Spanish.
        3. **SUMMARY**: Rewrite the 'summary' to be highly relevant to the job.
        4. **PROJECTS as EXPERIENCE**: The 'experience' section MUST be populated/replaced by the 'relevant_projects' identified in the analysis.
           - **Structure**: Use the "Experience" format: Role = Project Role, Company = Project Name.
           - **Content**: Use the detailed data from "Available Portfolio Projects" to write 3-4 powerful bullet points per project.
           - **TECH STACK**: EXPLICITLY MENTION the frameworks, languages, and tools used in EACH bullet point. CRITICAL: WRAP EVERY TECHNICAL TERM IN <b> TAGS (e.g., "Built REST API using <b>Node.js</b>/<b>Express</b>...", "Optimized <b>SQL Server</b> queries...").
           - **Quantity**: You MUST list exactly 3 project experiences.
           - **Fallback**: If 'relevant_projects' has fewer than 3 items, you MUST add "Mambo Fitness" (or "App Fitness") as the 3rd project. Tailor its description to highlight skills relevant to the vacancy.
        5. **SKILLS**: Assume the candidate has the 'missing_skills' if they are common in the stack and add them.
        
        Return ONLY a JSON object that matches the Master Profile schema + the "language" key.
        """
        response_text = self.provider.generate(prompt, system_prompt)
        try:
            # Robust extraction
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if json_match:
                clean_json = json_match.group(1)
            else:
                clean_json = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            return cv_json  # Fallback to original if AI fails
