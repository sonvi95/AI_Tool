import json
from pathlib import Path


class FileConfiguration():
    def __init__(self):
        self.path = Path("D:/code/configuration.json")

    def load_json(self):
        """
        Load JSON data from file.
        Returns `default` if file does not exist or error occurs.
        """
        try:
            if not self.path.exists():
                return {}

            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"[ERROR] Load JSON failed: {e}")
            return {}

    def save_json(self, data_json):
        """
        Save data to JSON file.
        Creates parent folders if needed.
        """
        try:
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"[ERROR] Save JSON failed: {e}")
            return False

FILE_CONFIGURATION = FileConfiguration()


