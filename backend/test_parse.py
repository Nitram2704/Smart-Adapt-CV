import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

class GroqProvider:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str, system_instruction: str = None) -> str:
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
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error connecting to Groq: {str(e)} - {response.text if 'response' in locals() else ''}"

# Mock text
sample_cv = "Martin Sanchez Urrego. Software Engineer. React, Python, Node.js. Worked at Mambo Fitness as Lead Developer."

system_prompt = "You are an expert AI CV Parser and ATS researcher."
prompt = f"Analyze the following CV text and extract it into a STRICT JSON format. CV Text: {sample_cv}"

provider = GroqProvider(os.getenv("GROQ_API_KEY"))
response_text = provider.generate(prompt, system_prompt)

print(f"Raw Response: {response_text}")

try:
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}')
    if start_idx != -1 and end_idx != -1:
        clean_json = response_text[start_idx:end_idx+1]
    else:
        clean_json = response_text
    
    result = json.loads(clean_json)
    print("Success!")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
