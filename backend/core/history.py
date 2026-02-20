import json
import os
from datetime import datetime
from uuid import uuid4

class HistoryManager:
    def __init__(self, storage_path="data/jobs_history.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as f:
                json.dump([], f)

    def add_entry(self, company, role, match_score, cv_filename, vacancy_summary):
        entry = {
            "id": str(uuid4()),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "company": company,
            "role": role,
            "match_score": match_score,
            "cv_filename": cv_filename,
            "vacancy_summary": vacancy_summary,
            "status": "Generated"
        }
        history = self.get_all()
        history.insert(0, entry)
        with open(self.storage_path, "w") as f:
            json.dump(history, f, indent=2)
        return entry

    def get_all(self):
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except:
            return []

    def update_status(self, entry_id, status):
        history = self.get_all()
        for entry in history:
            if entry["id"] == entry_id:
                entry["status"] = status
                with open(self.storage_path, "w") as f:
                    json.dump(history, f, indent=2)
                return True
        return False
