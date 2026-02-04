from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import shutil
import os
from dotenv import load_dotenv
from core.parser import extract_text_from_pdf, parse_text_to_master_profile
from core.ai_engine import AIEngine, OllamaProvider, GeminiProvider
from core.portfolio import load_portfolio_projects
from core.generator import render_cv_html, generate_pdf

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Smart-Adapt CV API")

# Mount outputs directory as static
# This is required for the frontend to download generated PDFs
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Validation Error: {exc.errors()}")
    print(f"Request Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(await request.body())},
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins. In production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(BASE_DIR, "inputs")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(INPUTS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any

class BasicInfo(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str
    email: Optional[Any] = ""
    phone: Optional[Any] = ""
    linkedin_url: Optional[Any] = ""
    github_url: Optional[Any] = ""
    portfolio_url: Optional[Any] = ""
    title: Optional[Any] = "Software Engineer"

class Experience(BaseModel):
    model_config = ConfigDict(extra='allow')
    company: Optional[Any] = "Unknown"
    role: Optional[Any] = "Role"
    duration: Optional[Any] = ""
    highlights: Optional[Any] = []
    stack: Optional[Any] = []

class Project(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: Optional[Any] = "Project"
    description: Optional[Any] = ""
    impact_metrics: Optional[Any] = None

class MasterProfile(BaseModel):
    model_config = ConfigDict(extra='allow')
    basic_info: BasicInfo
    summary: Optional[Any] = ""
    skills: Optional[Any] = {}
    experience: Optional[List[Any]] = []
    projects: Optional[List[Any]] = []

class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra='allow')
    vacancy_text: str
    profile: Any  # Allow any shape for profile to be safe

class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra='allow')
    profile: Any
    recommendations: Any

# Initialize AI Engine
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

if api_key:
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "****"
    print(f"DEBUG: Using Gemini Provider with masked key: {masked_key}")
    print(f"DEBUG: Active Model: gemini-2.0-flash")
    llm_provider = GeminiProvider(api_key=api_key)
else:
    print(f"Using Ollama Provider with model: {model_name}")
    llm_provider = OllamaProvider(model=model_name)
    
ai_engine = AIEngine(llm_provider)

@app.get("/")
async def root():
    return {"message": "Smart-Adapt CV API is running"}

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
        # Ensure profile is a dict
        profile_data = request.profile
        if hasattr(profile_data, "model_dump"):
            profile_data = profile_data.model_dump()
            
        analysis = ai_engine.analyze_cv_and_job(
            profile_data, 
            request.vacancy_text, 
            portfolio_projects
        )
        return {"analysis": analysis}
    except Exception as e:
        print(f"Error in /cv/analyze: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cv/generate")
async def generate_cv(request: GenerateRequest):
    try:
        # Ensure profile is a dict
        profile_data = request.profile
        if hasattr(profile_data, "model_dump"):
            profile_data = profile_data.model_dump()

        portfolio_projects = load_portfolio_projects()
        optimized_profile = ai_engine.generate_optimized_content(
            profile_data, 
            request.recommendations,
            portfolio_projects
        )
        
        html_content = render_cv_html(optimized_profile)
        output_filename = f"cv_optimized_{profile_data.get('basic_info', {}).get('name', 'optimized').replace(' ', '_')}.pdf"
        output_path = os.path.join(OUTPUTS_DIR, output_filename)
        
        generate_pdf(html_content, output_path)
        
        return {
            "message": "CV generated successfully",
            "filename": output_filename,
            "optimized_profile": optimized_profile
        }
    except Exception as e:
        print(f"Error in /cv/generate: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
