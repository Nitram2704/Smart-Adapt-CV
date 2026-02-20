import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

def list_free_models():
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        models = response.json()["data"]
        
        print("--- Available 'free' Models ---")
        count = 0
        for m in models:
            mid = m["id"]
            if ":free" in mid or "free" in m.get("pricing", {}).get("prompt", ""):
                 print(mid)
                 count += 1
        
        print(f"\nTotal Free Models Found: {count}")
        
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_free_models()
