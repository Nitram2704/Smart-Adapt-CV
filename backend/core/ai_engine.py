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

class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "response_format": {"type": "json_object"} if "JSON" in prompt else None
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            if response.status_code == 429:
                return "ERROR_QUOTA_EXCEEDED: Groq rate limit reached."
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"ERROR_PROVIDER_FAILED: {str(e)}"

class OpenRouterProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        # List of free models to try in order
        self.free_models = [
            "qwen/qwen-2.5-72b-instruct:free", # Extremely powerful for parsing/logic
            "google/gemma-3-27b-it:free",      # Very fast and efficient
            "meta-llama/llama-3.3-70b-instruct:free",
            "mistralai/mistral-small-3.1-24b-instruct:free",
            "deepseek/deepseek-r1-distill-llama-70b:free", # Reliable alternative to full R1
            "deepseek/deepseek-r1-0528:free", # Keep but at the bottom due to traffic
        ]
        # If a specific model is requested via env, put it first
        env_model = os.getenv("OPENROUTER_MODEL")
        if env_model:
            self.free_models.insert(0, env_model)
        
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://smart-adapt-cv.com", 
            "X-Title": "Smart Adapt CV"
        }
        
        errors = []
        
        for model in self.free_models:
            print(f"DEBUG: OpenRouter trying model: {model}")
            
            # Construct payload - be conservative to avoid 400s
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.1,
            }
            # Only add response_format for models known to support it well via OpenRouter, 
            # OR if we are getting 400s, it's safer to omit it and rely on the system prompt.
            # Many free models on OpenRouter do NOT support 'json_object' mode.
            # We will omit it to maximize compatibility.
            
            try:
                # 120s timeout for slower "thinking" models like Deepseek R1
                response = requests.post(self.url, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 429:
                    print(f"DEBUG: Model {model} rate limited (429). Trying next...")
                    errors.append(f"{model}: 429 Quota Exceeded")
                    continue
                    
                if response.status_code == 503 or response.status_code == 502:
                     print(f"DEBUG: Model {model} overloaded ({response.status_code}). Trying next...")
                     errors.append(f"{model}: {response.status_code} Overloaded")
                     continue

                if response.status_code == 400 or response.status_code == 404:
                    print(f"DEBUG: Model {model} error ({response.status_code}): {response.text}")
                    errors.append(f"{model}: {response.status_code} {response.text}")
                    continue

                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"DEBUG: Model {model} failed: {e}")
                errors.append(f"{model}: {str(e)}")
                continue

        return f"ERROR_PROVIDER_FAILED: All OpenRouter models failed. Details: {'; '.join(errors)}"

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3.2"):
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
            response = requests.post(self.url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"ERROR_PROVIDER_FAILED: Ollama offline/timeout. {str(e)}"

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model_20 = genai.GenerativeModel('gemini-2.0-flash')
        self.model_15 = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
        try:
            response = self.model_20.generate_content(full_prompt)
            return response.text
        except Exception as e:
            try:
                response = self.model_15.generate_content(full_prompt)
                return response.text
            except:
                if "429" in str(e):
                    return "ERROR_QUOTA_EXCEEDED: Gemini quota reached."
                return f"ERROR_PROVIDER_FAILED: Gemini error. {str(e)}"

class FallbackProvider(LLMProvider):
    def __init__(self, providers: List[LLMProvider]):
        self.providers = providers

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        errors = []
        for provider in self.providers:
            result = provider.generate(prompt, system_instruction)
            if "ERROR_" not in result:
                return result
            print(f"DEBUG: Provider {provider.__class__.__name__} failed: {result}")
            errors.append(result)
        
        return f"ERROR_ALL_PROVIDERS_FAILED: " + " | ".join(errors)

class AIEngine:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def analyze_cv_and_job(self, cv_json: Dict, job_text: str, portfolio_projects: List[Dict], certifications: List[Dict] = []) -> Dict:
        print(f"DEBUG: Analyzing job_text (len={len(job_text)}): {job_text[:50]}")
        # Pre-check
        clean_text = job_text.strip() if job_text else ""
        if not clean_text or len(clean_text) < 15: # Loosened from 30 to 15
            return {
                "match_score": 0,
                "missing_skills": [],
                "salary_expectation": {"min": 0, "max": 0, "currency": "USD", "reasoning": "Input too short."},
                "relevant_projects": [],
                "relevant_certifications": [],
                "relevant_tools": {"Backend": [], "Frontend": [], "Cloud": [], "Architecture": [], "Project_Management": []},
                "recommendations": "Please provide more details about the job.",
                "rubric_breakdown": {"hard_skills": 0, "experience": 0, "certifications": 0, "fit": 0},
                "detected_language": "en"
            }

        system_prompt = """You are a Senior Technical Recruiter. 
        Analyze the match between the CV and Job. 
        CRITICAL: Detect the language of the Job Vacancy (e.g., 'es' for Spanish, 'en' for English).
        All 'reasoning', 'recommendations', and 'reason' fields MUST be in the 'detected_language'.
        BE DYNAMIC: If the job description is broad, find the best overlap in skills. 
        DO NOT be unnecessarily harsh. If it's a valid job, give a fair score.
        
        PRIORITY NOTE: Treat 'Documentation Generator (docgen)', 'AutoQA', and 'App Fitness' as high-priority 'Hero Projects'.
        - 'docgen': Focus on RAG, AI Infrastructure, and Code Parsing.
        - 'AutoQA': Focus on Autonomous Agents, Self-healing Automation, and QA.
        - 'App Fitness': Focus on Mobile Development (React Native), UX, and robust complex systems.
        Nudge their relevance higher if they align with the job's core technical requirements."""
        
        prompt = f"""
        CV Data: {json.dumps(cv_json)}
        Job Vacancy: {job_text}
        Portfolio List: {json.dumps(portfolio_projects)}
        Certifications List: {json.dumps(certifications)}

        ANALYSIS REQUIREMENTS:
        1. **DETECT LANGUAGE**: Identify if the vacancy is 'es' or 'en'. Return this as `detected_language`.
        2. **MATCH SCORE RUBRIC (Total 100)**:
           - **Hard Skills (40 pts)**: Match technologies.
           - **Experience (30 pts)**: Match seniority/complexity.
           - **Certifications (15 pts)**: Value added.
           - **Fit (15 pts)**: Cultural/Tone fit.
        3. **SALARY ESTIMATION**: 
           - Detect Seniority and Region (default to Colombia if ambiguous).
           - Estimate ANNUAL range. 
           - **STRICT GUIDELINES for Colombia (COP)**:
             - **Practicante / Intern**: 1.3M - 2M COP monthly (15M - 24M COP/year).
             - **Junior / Entry**: 2.5M - 4.5M COP monthly (30M - 54M COP/year).
             - **Intermediate / Senior**: 6M - 15M+ COP monthly (72M - 180M+ COP/year).
           - Reasoning MUST be in the `detected_language`.
        4. **PORTFOLIO MATCHING**: Select the 3 most relevant projects. 
           - Prioritize projects with dates that align with the job's requirements or career timeline.
        5. **TOOLS**: Identify ALL relevant tools. Categories: "Backend", "Frontend", "Databases", "Cloud", "Architecture", "Project Management".
        6. **CERTIFICATIONS**: Match available certifications to the job requirements.

        RETURN JSON:
        {{
          "match_score": number,
          "detected_language": "string",
          "rubric_breakdown": {{ "hard_skills": number, "experience": number, "certifications": number, "fit": number }},
          "missing_skills": ["..."],
          "salary_expectation": {{ "min": number, "max": number, "currency": "USD", "reasoning": "..." }},
          "relevant_projects": [{{ "name": "...", "reason": "...", "id": "..." }}],
          "relevant_certifications": [{{"name": "...", "issuer": "...", "year": "...", "reason": "..."}}],
          "relevant_tools": {{ 
             "Backend": [], "Frontend": [], "Databases": [], "Cloud": [], "Architecture": [], "Project_Management": [] 
          }},
          "recommendations": "string",
          "seniority_detected": "string"
        }}
        """
        response_text = self.provider.generate(prompt, system_prompt)
        try:
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            clean_json = json_match.group(1) if json_match else response_text
            result = json.loads(clean_json)
            # Defaults
            result.setdefault("detected_language", "en")
            print(f"DEBUG: Analysis result language: {result['detected_language']}")
            return result
        except Exception as e:
            print(f"DEBUG: AI Analysis Parse Error: {e}")
            return {"error": "Failed to parse AI response", "raw": response_text}

    def generate_optimized_content(self, master_profile: dict, analysis: dict, portfolio_projects: dict, tone: str = "Professional", methodology: str = "STAR") -> dict:
        lang = analysis.get("detected_language", "en")
        
        # --- ROBUST PHYSICAL PROJECT FILTERING ---
        # 1. Build a pool of all possible experience descriptions
        original_experience = master_profile.get("experience", [])
        pool = []
        for p in original_experience:
            p["_source"] = "master"
            pool.append(p)
        for p in portfolio_projects:
            p["_source"] = "portfolio"
            pool.append(p)
            
        # 2. Extract relative identifiers from analysis
        relevant_recs = analysis.get("relevant_projects", [])
        rel_ids = [str(r.get("id", "")).lower().strip() for r in relevant_recs if r.get("id")]
        rel_names = [str(r.get("name", "")).lower().strip() for r in relevant_recs if r.get("name")]
        
        # 3. Filter the pool
        filtered_experience = []
        seen_names = set()
        
        for item in pool:
            name = str(item.get("name", item.get("company", ""))).lower().strip()
            item_id = str(item.get("id", "")).lower().strip()
            
            # Match by ID or Name (case-insensitive)
            is_match = False
            if item_id and item_id in rel_ids: is_match = True
            if name and (name in rel_names or name in rel_ids): is_match = True
            
            if is_match and name not in seen_names:
                filtered_experience.append(item)
                seen_names.add(name)
        
        # Safety/Fallback: If filtering returned nothing but analysis had recommendations, 
        # it means the matching failed. In that case, we MUST still try to include something.
        if not filtered_experience and relevant_recs:
            print(f"DEBUG: Project matching failed. Pool size: {len(pool)}. Rel Names: {rel_names}")
            # Fallback to the first 3 items in the pool or the original master experience
            filtered_experience = original_experience[:3]
            
        # 4. OVERRIDE Master Profile Experience with ONLY the filtered projects
        # This ensures the AI doesn't see "Mambo Fitness" if it wasn't selected
        master_profile["experience"] = filtered_experience
        
        # Localize default title if not provided or just "Software Engineer"
        prof_title = master_profile.get("basic_info", {}).get("title", "Software Engineer")
        if lang == "es" and prof_title == "Software Engineer":
            prof_title = "Ingeniero de Software"
        
        title_instruction = f'Use "{prof_title}" as the professional title in basic_info.title.'
        
        system_prompt = f"""You are an Expert Senior CV Writer and Technical Branding Specialist. 
        Language: {lang}. 
        Your goal is to transform standard career data into a high-impact document.
        {title_instruction}
        EVERYTHING (except proper names/tech) MUST be strictly in {lang}."""
        
        # Inject default English B2 and Spanish Native
        languages = master_profile.get("languages", [])
        
        # English
        eng_idx = next((i for i, l in enumerate(languages) if "English" in l.get("language", "") or "Inglés" in l.get("language", "")), None)
        if eng_idx is not None:
            languages[eng_idx]["level"] = "B2"
        else:
            languages.append({"language": "English" if lang == "en" else "Inglés", "level": "B2"})
        
        # Spanish
        spa_idx = next((i for i, l in enumerate(languages) if "Spanish" in l.get("language", "") or "Español" in l.get("language", "")), None)
        if spa_idx is not None:
            languages[spa_idx]["level"] = "Native" if lang == "en" else "Nativo"
        else:
            languages.append({"language": "Spanish" if lang == "en" else "Español", "level": "Native" if lang == "en" else "Nativo"})
        
        master_profile["languages"] = languages

        # Certifications from analysis
        relevant_certs = analysis.get("relevant_certifications", [])

        prompt = f"""
        Master Profile (FILTERED): {json.dumps(master_profile)}
        Analysis Context: {json.dumps(analysis)}
        
        OUTPUT LANGUAGE: {lang}. **DO NOT MIX LANGUAGES**.
        
        STRICT WRITING RULES (SENIOR PERSONA):
        0. **BOLD FORMATTING**: ONLY within the 'summary' and 'experience' highlights, when mentioning any framework, library, technology, tool (e.g., **C#**, **React**, **Docker**) or any quantified result/metric (e.g., **"reduced latency by 40%"**, **"95% test coverage"**), you MUST wrap it in `<strong>` tags (e.g., `<strong>C#</strong>`, `<strong>40%</strong>`).
        1. **MANDATORY QUANTIFICATION**: Every highlight MUST include at least one quantified result or scale indicator (e.g., "reduced latency by 40%", "managed 50k+ daily users", "achieved 95% test coverage").
        2. **IMPACT VERBS**: Use active and high-impact engineering verbs: *Architected, Orchestrated, Engineered, Deployed, Systematized, Optimized, Spearheaded*.
        3. **SINGLE STAR CONSTRAINT**: For each experience/project entry, you MUST provide EXACTLY ONE 'STAR' accomplishment. 
           - Choose the MOST RELEVANT technical accomplishment for the target job.
           - Return EXACTLY 4 bullet points total per experience entry (one for Situation, one for Task, one for Action, one for Result).
           - Do NOT repeat the STAR cycle. Do NOT provide multiple actions or results.
        4. **LANGUAGE ENFORCEMENT**: Every field (summary, roles, descriptions, reasons) MUST be in {lang}.
        5. **MANDATORY FIELDS**: For EACH experience entry, you MUST provide the `company` (Project/Company Name), `role`, `duration`, and `highlights`. DO NOT omit the company name.
        6. **PROJECTS / EXPERIENCE**: Redact highlights using the {methodology} method in {lang}.
           - CRITICAL: Use ONLY the projects identified as relevant in 'Analysis Context' (found in `relevant_projects`).
           - If there are fewer than 3 relevant projects, you may include the most recent experience entries to fill the space, but prioritize the relevant ones first.
           - Use EXACTLY FOUR BULLET POINTS PER ENTRY. 
           - **Structure per entry**:
             - Situation: [Strategic context]
             - Task: [The high-level technical challenge]
             - Action: [Sophisticated technical implementation]
             - Result: [Quantified achievement/Metric]
           - **CAREER TIMELINE STIPULATION (CRITICAL)**:
             - You MUST assign a realistic `duration` to each entry (e.g., "Jan 2022 - Present", "2020 - 2021"). 
             - **STRATEGY**: Detect the seniority required by the job (e.g., Senior = 5+ years). Distribute the selected projects/experience across that timeframe ending in 'Present' or 'Actual'.
             - If a project has a `year_hint` or `default_duration` in its data, respect that as a 'reality anchor' but adapt the months/years to form a continuous, logical career path without gaps.
             - Use the format appropriate for the language (e.g., "Ene 2023 - Actual" for 'es', "Jan 2023 - Present" for 'en').
           - Ensure 4-8 high-impact bullet points total per project (e.g., repeating the STAR cycle for different features).
           - Do NOT use the pipe separator (|). Use individual line breaks.
           - Use advanced technical terminology suitable for Senior/Lead roles.
        3. **CERTIFICATIONS**: Include the following certifications which were identified as relevant: {json.dumps(relevant_certs)}.
           - Also include any relevant certifications from the master profile.
        4. **TOOLS & SKILLS ENRICHMENT**:
           - **HARVESTING**: Extract EVERY technical tool, library, and framework mentioned in the Experience and Portfolio sections.
           - **VACANCY ALIGNMENT**: Identify the top 3-5 most critical technologies mentioned in the 'Analysis Context' (vacancy) that the user should highlight. Even if not explicitly in the Master Profile, if they are relevant to the user's domain (e.g., a backend tool for a backend dev), include them as 'Target Skills' or integrated into the categories.
           - **COMPREHENSIVENESS**: Build a VERY DENSE 'skills' object. Do NOT be selective. Aim for 6-10 items per category if they are mentioned anywhere in the source data.
           - **PRIORITY**: If the Vacancy asks for a skill and it's in the Master Profile, it MUST be first in its category.

        Return the optimized JSON following this structure:
        {{
          "basic_info": {{ 
             "portfolio_url": "...", "linkedin_url": "...", "github_url": "...", "phone": "...", "email": "...", "name": "..." 
          }},
          "summary": "...",
          "skills": {{ 
             "backend": [], "frontend": [], "databases": [], "cloud": [], "architecture": [], "project_management": [] 
          }},
          "certifications": [{{ "name": "...", "issuer": "...", "year": "..." }}],
          "education": [{{ "institution": "...", "degree": "...", "year": "..." }}],
          "experience": [{{ "company": "...", "role": "...", "duration": "...", "highlights": ["..."] }}],
          "languages": [{{ "language": "...", "level": "..." }}]
        }}
        """
        response_text = self.provider.generate(prompt, system_prompt)
        
        optimized = {}
        try:
            # IMPROVED JSON EXTRACTION
            # Try to find JSON within code blocks first
            code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if code_block_match:
                clean_json = code_block_match.group(1)
            else:
                # Fallback to finding first { and last }
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    clean_json = response_text[start_idx:end_idx+1]
                else:
                    print(f"DEBUG: Could not find JSON braces in AI response. Raw: {response_text[:100]}...")
                    clean_json = response_text # Attempt parsing anyway

            optimized = json.loads(clean_json)
        except Exception as e:
            print(f"DEBUG: AI Generation Parse Error: {e}")
            print(f"DEBUG: Raw AI Response that failed: {response_text}")
            # Initialize empty optimized to trigger fallback merge
            optimized = {}

        # --- ROBUST MERGE STRATEGY ---
        try:
             # NORMALIZE KEYS (Fix for Spanish/English mismatch)
            key_map = {
                # Basic Info
                "perfil": "basic_info",
                "datos_básicos": "basic_info",
                "datos_personales": "basic_info",
                "información_personal": "basic_info",
                
                # Summary
                "resumen": "summary",
                "perfil_profesional": "summary",
                "resumen_profesional": "summary",
                
                # Skills
                "habilidades": "skills",
                "conocimientos": "skills",
                "competencias": "skills",
                "tecnologías": "skills",
                
                # Experience
                "experiencia": "experience",
                "experiencia_profesional": "experience",
                "experiencia_laboral": "experience",
                "proyectos": "experience", # Sometimes AI puts projects at top level
                
                # Education
                "educación": "education",
                "educacion": "education",
                "formación": "education",
                "formacion": "education",
                "estudios": "education",
                
                # Certifications
                "certificaciones": "certifications",
                "certificados": "certifications",
                
                # Languages
                "idiomas": "languages",
                "lenguajes": "languages"
            }

            # Normalize top-level keys
            for key in list(optimized.keys()):
                lower_key = key.lower()
                if lower_key in key_map:
                    standard_key = key_map[lower_key]
                    if standard_key not in optimized: # Don't overwrite if English key exists
                        print(f"DEBUG: Normalizing key '{key}' -> '{standard_key}'")
                        optimized[standard_key] = optimized.pop(key)

            # Normalize specific inner keys (like 'experiencia' items)
            if "experience" in optimized and isinstance(optimized["experience"], list):
                for item in optimized["experience"]:
                    # Role/Title
                    if "rol" in item and "role" not in item: item["role"] = item.pop("rol")
                    if "cargo" in item and "role" not in item: item["role"] = item.pop("cargo")
                    # Company / Project
                    if "empresa" in item and "company" not in item: item["company"] = item.pop("empresa")
                    if "proyecto" in item and "company" not in item: item["company"] = item.pop("proyecto")
                    if "nombre_proyecto" in item and "company" not in item: item["company"] = item.pop("nombre_proyecto")
                    # Duration
                    if "duración" in item and "duration" not in item: item["duration"] = item.pop("duración")
                    if "periodo" in item and "duration" not in item: item["duration"] = item.pop("periodo")
                    if "fecha" in item and "duration" not in item: item["duration"] = item.pop("fecha")
                    # Highlights
                    if "logros" in item and "highlights" not in item: item["highlights"] = item.pop("logros")
                    if "descripción" in item and "highlights" not in item: item["highlights"] = item.pop("descripción")
                    if "descripcion" in item and "highlights" not in item: item["highlights"] = item.pop("descripcion")
                    if "responsabilidades" in item and "highlights" not in item: item["highlights"] = item.pop("responsabilidades")
            
            # Normalize Skills if it's a list instead of dict (Common mistake)
            if "skills" in optimized and isinstance(optimized["skills"], list):
                print("DEBUG: formatted skills list to dict")
                new_skills = {"backend": [], "frontend": [], "databases": [], "cloud": [], "architecture": [], "project_management": []}
                # Try to distribute or just put in backend
                new_skills["backend"] = optimized["skills"]
                optimized["skills"] = new_skills

            # Helper to check if a value is "empty" (None, empty list, empty dict, empty string)
            def is_empty(val):
                if val is None: return True
                if isinstance(val, (str, list, dict)) and len(val) == 0: return True
                return False

            # Mandatory keys for the template
            keys_to_check = ["basic_info", "summary", "skills", "certifications", "education", "experience", "languages"]
            
            for key in keys_to_check:
                ai_val = optimized.get(key)
                master_val = master_profile.get(key)
                
                # Special Case: Skills should be a MERGE (Additive), not a replacement
                if key == "skills":
                    print("DEBUG: Merging Skills (AI + Master)")
                    merged_skills = {}
                    ai_skills = ai_val if isinstance(ai_val, dict) else {}
                    master_skills = master_val if isinstance(master_val, dict) else {}
                    
                    # Categories to iterate
                    categories = set(list(ai_skills.keys()) + list(master_skills.keys()))
                    for cat in categories:
                        ai_list = ai_skills.get(cat, [])
                        master_list = master_skills.get(cat, [])
                        # Ensure they are lists
                        if not isinstance(ai_list, list): ai_list = [ai_list] if ai_list else []
                        if not isinstance(master_list, list): master_list = [master_list] if master_list else []
                        
                        # Merge unique items, case insensitive, stripping HTML for comparison
                        seen = set()
                        final_list = []
                        for item in (ai_list + master_list):
                            # Strip <strong> tags for accurate comparison
                            clean_item = re.sub(r'</?strong>', '', str(item), flags=re.IGNORECASE).lower().strip()
                            if clean_item not in seen:
                                final_list.append(item)
                                seen.add(clean_item)
                        merged_skills[cat] = final_list
                        print(f"DEBUG: Category '{cat}' merged count: {len(final_list)}")
                    optimized["skills"] = merged_skills
                    continue

                # Fallback for other sections (Experience, Summary, etc.)
                if is_empty(ai_val): 
                    if not is_empty(master_val):
                        print(f"DEBUG: AI missed or returned empty '{key}'. Fallback to Master data.")
                        optimized[key] = master_val
                elif key == "basic_info" and isinstance(ai_val, dict) and isinstance(master_val, dict):
                    # Deep merge for basic_info sub-fields (Social Links)
                    print("DEBUG: Deep merging basic_info (Links/Contact)")
                    link_keys = ["portfolio_url", "linkedin_url", "github_url", "phone", "email"]
                    for lk in link_keys:
                        if is_empty(ai_val.get(lk)) and not is_empty(master_val.get(lk)):
                            print(f"DEBUG: Restoring missing link/field '{lk}' from Master")
                            ai_val[lk] = master_val[lk]
                            
                elif key == "experience" and isinstance(ai_val, list) and isinstance(master_val, list):
                    # Field-level merge for experience items
                    print(f"DEBUG: Field-level merge for experience entries (AI={len(ai_val)}, Master={len(master_val)})")
                    for i, ai_item in enumerate(ai_val):
                        if i < len(master_val):
                            master_item = master_val[i]
                            # If AI missed company but master has it, restore it
                            if is_empty(ai_item.get("company")) and not is_empty(master_item.get("company")):
                                ai_item["company"] = master_item["company"]
                            # If AI missed duration but master has it, restore it
                            if is_empty(ai_item.get("duration")) and not is_empty(master_item.get("duration")):
                                ai_item["duration"] = master_item["duration"]
                            # If AI missed role but master has it, restore it
                            if is_empty(ai_item.get("role")) and not is_empty(master_item.get("role")):
                                ai_item["role"] = master_item["role"]

            optimized["language"] = lang # Ensure singular 'language' is present for template
            
            print(f"DEBUG: Final Optimized JSON keys: {list(optimized.keys())}")
            # Debug sizes
            print(f"DEBUG: Experience entries: {len(optimized.get('experience', []))}")
            print(f"DEBUG: Skills categories: {list(optimized.get('skills', {}).keys())}")
            
            return optimized

        except Exception as e:
            print(f"DEBUG: Critical Error in Merge Logic: {e}")
            # Ultimate Fallback: Return Master Profile but ensure language is set
            master_profile["language"] = lang
            return master_profile

    def generate_cover_letter(self, master_profile: dict, job_text: str, analysis: dict) -> dict:
        lang = analysis.get("detected_language", "en")
        system_prompt = f"You are an expert executive letter writer. Language: {lang}."
        prompt = f"""
        Generate a compelling cover letter in '{lang}'.
        Profile: {json.dumps(master_profile)}
        Job: {job_text}
        Analysis: {json.dumps(analysis)}

        CRITICAL: 
        1. **LANGUAGE**: The entire content MUST be in '{lang}'.
        2. **DYNAMISM**: Reference specific projects from the 'relevant_projects' list.
        3. **STRUCTURE**: Professional and results-oriented.

        Return a JSON object with:
        {{
            "date": "string",
            "recipient": "Hiring Manager",
            "content": "string (multiline)",
            "closing": "string"
        }}
        """
        response_text = self.provider.generate(prompt, system_prompt)
        try:
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            clean_json = json_match.group(1) if json_match else response_text
            return json.loads(clean_json)
        except:
            if lang == "es":
                return {"error": "Error de generación", "content": "Estimado Responsable de Selección..."}
            return {"error": "Generation failed", "content": "Dear Hiring Manager..."}

    def interpret_target_goal(self, goal_text: str) -> Dict:
        """
        Proactively interprets a vague goal (e.g., 'Tesla', 'Fintech') and generates 
        a high-impact synthetic vacancy description.
        """
        system_prompt = "You are an Expert Corporate Intelligence Agent and Technical Recruiter. Your goal is to interpret vague career goals and generate a highly realistic, high-impact job description that reflects the target company's culture and tech stack."
        
        prompt = f"""
        Analyze the following user goal and generate a 'Synthetic Vacancy'.
        USER GOAL: {goal_text}

        Your output must be a JSON with:
        {{
          "interpreted_role": "Calculated role title",
          "synthetic_vacancy": "A 300-500 word realistic job description including: Company Mission, Tech Stack, Key Responsibilities, and Desired Impact.",
          "proactive_tips": ["Tip 1", "Tip 2"]
        }}

        INSTRUCTIONS:
        1. If the goal is just a company (e.g., 'Google'), assume a 'Software Engineer' role unless specified.
        2. Research (using your internal knowledge) the company's tech stack (e.g., Google = Go, C++, Python; Netflix = Java, Node.js).
        3. Include cultural keywords (e.g., Amazon = Leadership Principles; Tesla = First Principles).
        4. Be proactive: Suggest 2-3 tips on how to improve the CV specifically for this target.
        5. Return ONLY the JSON.
        """
        
        response = self.provider.generate(prompt, system_prompt)
        try:
            # Robust JSON extraction
            import re
            json_match = re.search(r'(\{.*\})', response, re.DOTALL)
            clean_json = json_match.group(1) if json_match else response
            
            # Remove any trailing junk if needed
            if "```" in clean_json:
                clean_json = clean_json.split("```")[0].strip()
                
            return json.loads(clean_json)
        except Exception as e:
            print(f"DEBUG: Goal Interpretation Parse Error: {e}")
            return {
                "interpreted_role": "Software Engineer",
                "synthetic_vacancy": f"Synthetic Vacancy for: {goal_text}. Focus on technical excellence and high-impact results.",
                "proactive_tips": ["Alinea tus proyectos con el stack tecnológico de la empresa.", "Cuantifica tus resultados técnicos y de negocio."]
            }

    def optimize_highlight(self, highlight_text: str, target_keyword: str, language: str = "en") -> str:
        """
        Rewrites a single highlight/bullet point to naturally incorporate a target keyword.
        """
        system_prompt = f"You are an Expert CV Writer. Your goal is to integrate a keyword into an existing achievement while maintaining professional tone and metric focus. Language: {language}."
        
        prompt = f"""
        Original Achievement: {highlight_text}
        Target Keyword: {target_keyword}
        
        TASK:
        Rewrite the achievement to naturally include the keyword. 
        Keep it concise, quantified, and technical.
        Return ONLY the rewritten text, no explanations. 
        MANDATORY: Use `<strong>` and `</strong>` tags around technologies and quantified metrics.
        """
        
        rewritten = self.provider.generate(prompt, system_prompt)
        return rewritten.strip().strip('"').strip("'")

    def suggest_keyword_placement(self, profile: Dict, keyword: str, language: str = "en") -> Dict:
        """
        Determines the best place to integrate a keyword (Skills vs specific Experience bullets).
        """
        system_prompt = f"You are an Expert Technical Branding Specialist. Your mission is to find the most impactful and natural place to integrate a keyword into a professional profile. Language: {language}."
        
        prompt = f"""
        Profile Data: {json.dumps(profile)}
        Target Keyword: {keyword}
        
        TASK:
        Analyze the profile and decide:
        1. **Skills**: Which category (backend, frontend, cloud, etc.) should this keyword belong to?
        2. **Experience**: Identify up to 2 specific bullet points (highlights) in the work history where this keyword would fit most naturally.
        
        RETURN JSON:
        {{
          "skill_suggestion": {{
             "category": "string (e.g., 'backend')",
             "reason": "short explanation"
          }},
          "experience_suggestions": [
            {{
              "company": "company name",
              "original_highlight": "exact text from profile",
              "suggested_rewrite": "rewritten bullet including the keyword with <strong> tags",
              "reason": "why it fits here"
            }}
          ]
        }}
        """
        
        response = self.provider.generate(prompt, system_prompt)
        try:
            json_match = re.search(r'(\{.*\})', response, re.DOTALL)
            clean_json = json_match.group(1) if json_match else response
            return json.loads(clean_json)
        except Exception as e:
            print(f"DEBUG: Keyword Suggestion Parse Error: {e}")
            return {"error": "Failed to analyze placement"}
