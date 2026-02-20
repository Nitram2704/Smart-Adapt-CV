import os
import json
import sys
from dotenv import load_dotenv

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from core.ai_engine import GroqProvider, GeminiProvider, OllamaProvider, OpenRouterProvider, FallbackProvider, AIEngine
from core.portfolio import load_portfolio_projects

load_dotenv()

# Setup Fallback (Priority: Groq > Gemini > Ollama)
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
groq_api_keys = [
    os.getenv("GROQ_API_KEY"), 
    os.getenv("GROQ_API_KEY_2"), 
    os.getenv("GROQ_API_KEY_3"),
    os.getenv("GROQ_API_KEY_4"),
    os.getenv("GROQ_API_KEY_5"),
    os.getenv("GROQ_API_KEY_6")
]
gemini_api_keys = [os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_API_KEY_2"), os.getenv("GOOGLE_API_KEY_3")]
ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")

providers = []
if openrouter_api_key:
    providers.append(OpenRouterProvider(api_key=openrouter_api_key, model="google/gemma-3-27b-it:free"))
    
for key in groq_api_keys:
    if key:
        providers.append(GroqProvider(api_key=key))
        
for key in gemini_api_keys:
    if key:
        providers.append(GeminiProvider(api_key=key))
providers.append(OllamaProvider(model=ollama_model))

llm_provider = FallbackProvider(providers)
ai_engine = AIEngine(llm_provider)

# Mock Data
master_profile = {
    "basic_info": {
        "name": "Martin Sanchez Urrego",
        "title": "Software Engineer",
        "email": "martin@example.com",
        "phone": "123456789"
    },
    "education": [{"institution": "Universidad X", "degree": "Ingeniero", "year": "2020"}],
    "experience": [{"company": "Prev Company", "role": "Dev", "duration": "2 years", "highlights": ["Did stuff"]}],
    "languages": [{"language": "Spanish", "level": "Native"}]
}

analysis = {
    "detected_language": "es",
    "relevant_certifications": [],
    "relevant_projects": []
}

portfolio_projects = load_portfolio_projects()

print("--- Testing Optimized CV Generation ---")
optimized = ai_engine.generate_optimized_content(
    master_profile, 
    analysis, 
    portfolio_projects,
    tone="Professional",
    methodology="STAR"
)

print("\n--- OPTIMIZED RESULT KEYS ---")
print(list(optimized.keys()))

print("\n--- OPTIMIZED CONTENT (SUMMARY) ---")
print(f"Summary: {optimized.get('summary')[:100] if optimized.get('summary') else 'MISSING'}")
print(f"Experience Count: {len(optimized.get('experience', []))}")
print(f"Skills: {optimized.get('skills')}")

if not optimized.get('experience') or not optimized.get('summary'):
    print("\nWARNING: Result appears empty!")
else:
    print("\nSuccess: Result contains data.")
