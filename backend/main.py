from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import shutil
import os
from datetime import datetime
from dotenv import load_dotenv
from core.parser import extract_text_from_pdf, parse_text_to_master_profile
from core.ai_engine import AIEngine, OllamaProvider, GeminiProvider, GroqProvider, OpenRouterProvider, FallbackProvider
from core.portfolio import load_portfolio_projects, load_certifications
from core.generator import render_cv_html, generate_pdf
from core.history import HistoryManager
from core.config_manager import ConfigManager, UserConfig
from core.locales import get_labels
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(BASE_DIR, "inputs")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(INPUTS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

app = FastAPI(title="Smart-Adapt CV API")

# Mount outputs directory as static
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Managers
history_manager = HistoryManager()
config_manager = ConfigManager()

# Initialize AI Engine — Priority: Groq > Gemini > OpenRouter > Ollama
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
groq_api_keys = [
    os.getenv("GROQ_API_KEY"), 
    os.getenv("GROQ_API_KEY_2"), 
    os.getenv("GROQ_API_KEY_3"),
    os.getenv("GROQ_API_KEY_4"),
    os.getenv("GROQ_API_KEY_5"),
    os.getenv("GROQ_API_KEY_6")
]
gemini_api_keys = [os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_API_KEY_2"), os.getenv("GOOGLE_API_KEY_3"), os.getenv("GOOGLE_API_KEY_4")]
ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")

providers = []

# Priority 1: Groq (Low Latency / High Speed)
for key in groq_api_keys:
    if key:
        providers.append(GroqProvider(api_key=key))

# Priority 2: Gemini (High Intelligence / Large Window)
for key in gemini_api_keys:
    if key:
        providers.append(GeminiProvider(api_key=key))

# Priority 3: OpenRouter (Fallback to various models)
if openrouter_api_key:
    providers.append(OpenRouterProvider(api_key=openrouter_api_key))

# Priority 4: Ollama (Local Offline Fallback)
providers.append(OllamaProvider(model=ollama_model))

llm_provider = FallbackProvider(providers)
ai_engine = AIEngine(llm_provider)

class AnalysisRequest(BaseModel):
    vacancy_text: str
    profile: Any

class GenerateRequest(BaseModel):
    profile: Any
    recommendations: Any
    vacancy_text: Optional[str] = ""
    tone: Optional[str] = "Professional"
    methodology: Optional[str] = "STAR"

class TargetGoalRequest(BaseModel):
    goal_text: str

class OptimizeHighlightRequest(BaseModel):
    highlight_text: str
    target_keyword: str
    language: Optional[str] = "en"

@app.get("/")
async def root():
    return {"message": "Smart-Adapt CV API is running", "provider": llm_provider.__class__.__name__}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/config")
async def get_config():
    return config_manager.get_config()

@app.post("/config")
async def update_config(config: UserConfig):
    return config_manager.update_config(config.model_dump())

@app.get("/history")
async def get_history():
    return history_manager.get_all()

@app.post("/cv/parse")
async def parse_cv(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    upload_path = os.path.join(INPUTS_DIR, file.filename)
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(upload_path)
    profile = parse_text_to_master_profile(text, llm_provider)
    return {"profile": profile}

@app.post("/cv/analyze")
async def analyze_vacancy(request: AnalysisRequest):
    try:
        portfolio_projects = load_portfolio_projects()
        certifications = load_certifications()
        analysis = ai_engine.analyze_cv_and_job(request.profile, request.vacancy_text, portfolio_projects, certifications)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cv/interpret-goal")
async def interpret_goal(request: TargetGoalRequest):
    try:
        print(f"DEBUG: /cv/interpret-goal called for: {request.goal_text}")
        result = ai_engine.interpret_target_goal(request.goal_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cv/generate")
async def generate_cv(request: GenerateRequest):
    try:
        print(f"DEBUG: /cv/generate called.")
        print(f"DEBUG: Request Profile Keys: {list(request.profile.keys())}")
        if "experience" in request.profile:
             print(f"DEBUG: Request Profile Experience Count: {len(request.profile['experience'])}")
        
        # Phone Number Fail-safe
        if "basic_info" in request.profile:
            current_phone = str(request.profile["basic_info"].get("phone", ""))
            if "3042621" in current_phone.replace(" ", ""):
                print(f"DEBUG: Correcting phone number from {current_phone} to +57 304 2621096")
                request.profile["basic_info"]["phone"] = "+57 304 2621096"
        
        if not request.recommendations or "error" in request.recommendations:
            print("ERROR: Invalid Recommendations in Request")
            raise HTTPException(status_code=400, detail="Cannot generate CV without a valid vacancy analysis.")

        portfolio_projects = load_portfolio_projects()
        print(f"DEBUG: Loaded {len(portfolio_projects)} portfolio projects.")
        
        current_date_str = datetime.now().strftime("%B %Y")
        optimized = ai_engine.generate_optimized_content(
            request.profile, 
            request.recommendations, 
            portfolio_projects,
            tone=request.tone,
            methodology=request.methodology,
            current_date=current_date_str
        )
        
        print("DEBUG: --- OPTIMIZED CONTENT STRUCTURE ---")
        print(f"DEBUG: Keys: {list(optimized.keys())}")
        print(f"DEBUG: Basic Info: {optimized.get('basic_info', {}).get('name', 'N/A')}")
        print(f"DEBUG: Experience Entries: {len(optimized.get('experience', []))}")
        if optimized.get('experience'):
            print(f"DEBUG: First Experience Role: {optimized['experience'][0].get('role', 'N/A')}")
        print(f"DEBUG: Skills Categories: {list(optimized.get('skills', {}).keys())}")
        print(f"DEBUG: Certifications Count: {len(optimized.get('certifications', []))}")
        print(f"DEBUG: Education Count: {len(optimized.get('education', []))}")
        print("DEBUG: -----------------------------------")
        
        lang = request.recommendations.get("detected_language", "en")
        optimized["labels"] = get_labels(lang)
        html = render_cv_html(optimized)
        
        # Verify HTML content briefly
        if "EXPERIENCIA" not in html and "EXPERIENCE" not in html:
            print("WARNING: 'EXPERIENCE' section missing from generated HTML!")

        safe_name = request.profile.get("basic_info", {}).get("name", "optimized").replace(" ", "_")
        filename = f"cv_{safe_name}.pdf"
        
        # DEBUG: Save HTML to inspect rendering issues
        debug_html_path = os.path.join(OUTPUTS_DIR, f"cv_debug_{safe_name}.html")
        with open(debug_html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"DEBUG: Saved HTML debug file to: {debug_html_path}")
        
        if optimized.get('experience') and len(optimized['experience']) > 0:
             print(f"DEBUG: First Experience Item Keys: {list(optimized['experience'][0].keys())}")
             print(f"DEBUG: First Experience Item Highlights Type: {type(optimized['experience'][0].get('highlights'))}")

        generate_pdf(html, os.path.join(OUTPUTS_DIR, filename))
        
        # Save History
        history_manager.add_entry(
            company=request.recommendations.get("company_name", "Unknown"),
            role=request.recommendations.get("job_role", "Unknown"),
            match_score=request.recommendations.get("match_score", 0),
            cv_filename=filename,
            vacancy_summary=request.vacancy_text[:100]
        )
        
        return {"filename": filename, "optimized_profile": optimized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cv/generate-ats")
async def generate_cv_ats(request: GenerateRequest):
    try:
        print(f"DEBUG: /cv/generate-ats called.")
        portfolio_projects = load_portfolio_projects()
        
        current_date_str = datetime.now().strftime("%B %Y")
        optimized = ai_engine.generate_optimized_content(
            request.profile, 
            request.recommendations, 
            portfolio_projects,
            tone=request.tone,
            methodology=request.methodology,
            current_date=current_date_str
        )
        
        # Use the NEW ATS template
        lang = optimized.get("language", "en")
        optimized["labels"] = get_labels(lang)
        html = render_cv_html(optimized, template_name="ats_foreign_template.html")
        
        safe_name = request.profile.get("basic_info", {}).get("name", "optimized").replace(" ", "_")
        filename = f"cv_ats_{safe_name}.pdf"
        
        generate_pdf(html, os.path.join(OUTPUTS_DIR, filename))
        
        return {"filename": filename, "optimized_profile": optimized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cv/generate-cl")
async def generate_cl(request: GenerateRequest):
    try:
        current_date_str = datetime.now().strftime("%B %Y")
        cl_data = ai_engine.generate_cover_letter(
            request.profile, 
            request.vacancy_text, 
            request.recommendations,
            current_date=current_date_str
        )
        
        # Structure data for the template
        lang = request.recommendations.get("detected_language", "en")
        template_data = {
            "language": lang,
            "candidate_info": {
                "name": request.profile.get("basic_info", {}).get("name", "Candidate"),
                "title": request.profile.get("basic_info", {}).get("title", "Developer"),
                "email": request.profile.get("basic_info", {}).get("email", ""),
                "phone": request.profile.get("basic_info", {}).get("phone", ""),
                "linkedin_url": request.profile.get("basic_info", {}).get("linkedin", "")
            },
            "date": cl_data.get("date", current_date_str),
            "recipient_info": {
                "hiring_manager": cl_data.get("recipient", "Hiring Manager"),
                "company_name": request.recommendations.get("company_name", "the Team")
            },
            "content_body": cl_data.get("content", "").replace("\n", "<br>")
        }

        from core.generator import render_cover_letter_html
        html = render_cover_letter_html(template_data)
        safe_name = request.profile.get("basic_info", {}).get("name", "optimized").replace(" ", "_")
        filename = f"cl_{safe_name}.pdf"
        generate_pdf(html, os.path.join(OUTPUTS_DIR, filename))
        return {"filename": filename, "content": cl_data}
    except Exception as e:
        print(f"CL Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/suggest-placement")
async def suggest_keyword_placement(request: Request):
    """
    Endpoint for the Keyword Booster extension.
    Suggests where to place a keyword (Experience vs Skills).
    """
    try:
        data = await request.json()
        profile = data.get("profile")
        keyword = data.get("keyword")
        language = data.get("language", "es")
        
        if not profile or not keyword:
            raise HTTPException(status_code=400, detail="Profile and keyword are required")
            
        suggestions = ai_engine.suggest_keyword_placement(profile, keyword, language)
        return suggestions
    except Exception as e:
        print(f"ERROR in suggest_placement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/optimize-highlight")
async def optimize_highlight(request: Request):
    """
    Optimizes a specific highlight with a keyword.
    """
    try:
        data = await request.json()
        highlight = data.get("highlight")
        keyword = data.get("keyword")
        language = data.get("language", "es")
        
        if not highlight or not keyword:
            raise HTTPException(status_code=400, detail="Highlight and keyword are required")
            
        optimized = ai_engine.optimize_highlight(highlight, keyword, language)
        return {"optimized_content": optimized}
    except Exception as e:
        print(f"ERROR in optimize_highlight: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use the port from environment variables or 8000 as default
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
