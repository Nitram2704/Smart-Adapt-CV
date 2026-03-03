import requests
import json

BASE_URL = "http://localhost:8000"

def test_keyword_extension():
    # Mock Profile Data
    profile = {
        "basic_info": {"name": "Test User", "title": "Software Engineer"},
        "experience": [
            {
                "company": "Tech Corp",
                "role": "Backend Dev",
                "highlights": ["Developed microservices using Python.", "Managed PostgreSQL databases."]
            }
        ],
        "skills": {
            "backend": ["Python", "PostgreSQL"]
        }
    }
    
    keyword = "Docker"
    
    print(f"\n--- Testing /ai/suggest-placement with keyword: {keyword} ---")
    response = requests.post(f"{BASE_URL}/ai/suggest-placement", json={
        "profile": profile,
        "keyword": keyword,
        "language": "es"
    })
    
    if response.status_code == 200:
        print("SUCCESS: Endpoint responded 200 OK")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"FAILURE: Status {response.status_code}")
        print(response.text)

    print(f"\n--- Testing /ai/optimize-highlight ---")
    highlight = "Developed microservices using Python."
    response = requests.post(f"{BASE_URL}/ai/optimize-highlight", json={
        "highlight": highlight,
        "keyword": keyword,
        "language": "es"
    })
    
    if response.status_code == 200:
        print("SUCCESS: Endpoint responded 200 OK")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"FAILURE: Status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        test_keyword_extension()
    except Exception as e:
        print(f"Could not connect to backend: {e}")
