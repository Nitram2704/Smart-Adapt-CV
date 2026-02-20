import json
import os

class ConfigManager:
    def __init__(self, config_path="data/user_config.json"):
        self.config_path = config_path
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                json.dump({"api_priority": ["groq", "gemini", "ollama"], "default_tone": "Professional"}, f)

    def get_config(self):
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except:
            return {}

    def update_config(self, new_config):
        current = self.get_config()
        current.update(new_config)
        with open(self.config_path, "w") as f:
            json.dump(current, f, indent=2)
        return current

from pydantic import BaseModel
class UserConfig(BaseModel):
    api_priority: list
    default_tone: str
