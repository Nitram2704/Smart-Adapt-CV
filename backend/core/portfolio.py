import os
import json
from typing import List, Dict

PORTFOLIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "portfolio")

def load_portfolio_projects() -> List[Dict]:
    """Loads all JSON files from the portfolio directory."""
    projects = []
    if not os.path.exists(PORTFOLIO_DIR):
        os.makedirs(PORTFOLIO_DIR, exist_ok=True)
        return projects

    for filename in os.listdir(PORTFOLIO_DIR):
        if filename.endswith(".json"):
            path = os.path.join(PORTFOLIO_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    project_data = json.load(f)
                    projects.append(project_data)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return projects
