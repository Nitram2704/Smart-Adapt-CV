import os
import sys
from dotenv import load_dotenv

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from core.ai_engine import GroqProvider, GeminiProvider, OllamaProvider, FallbackProvider, AIEngine
from core.parser import extract_text_from_pdf, parse_text_to_master_profile

load_dotenv()

# Setup Fallback (Priority: Groq > Gemini > Ollama)
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_keys = [os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_API_KEY_2"), os.getenv("GOOGLE_API_KEY_3")]
ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")

providers = []
if groq_api_key:
    providers.append(GroqProvider(api_key=groq_api_key))

for key in gemini_api_keys:
    if key:
        providers.append(GeminiProvider(api_key=key))

providers.append(OllamaProvider(model=ollama_model))

llm_provider = FallbackProvider(providers)

pdf_path = "c:\\Users\\marti\\Visual\\Smart-Adapt-CV\\backend\\inputs\\Martin Sanchez Urrego CV.pdf"

print(f"--- Testing Fallback System with {os.path.basename(pdf_path)} ---")
text = extract_text_from_pdf(pdf_path)

try:
    # This should now fallback to Gemini if Groq returns 429
    profile = parse_text_to_master_profile(text, llm_provider)
    print("--- PARSING RESULT ---")
    import json
    # Check if we got a real name or an error
    print(f"Detected Name: {profile.get('basic_info', {}).get('name')}")
    if profile.get('basic_info', {}).get('name') == "Error Parsing CV":
         print(f"Summary: {profile.get('summary')}")
    else:
         print("Success! Data extracted via Fallback System.")
except Exception as e:
    print(f"Test Failed: {e}")
