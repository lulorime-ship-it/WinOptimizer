import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".WinOptimizer"
        self.config_file = self.config_dir / "config.json"
        self.config = self.load_config()

    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()

    def get_default_config(self):
        return {
            "optimization_profile": "balanced",
            "auto_save": True,
            "show_notifications": True,
            "backup_before_optimize": True,
            "optimization_items": {},
            "cleanup_paths": {
                "temp": True,
                "prefetch": True,
                "recent": False,
                "logs": True,
                "thumbnails": True
            }
        }

    def save_config(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def export_config(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def import_config(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.save_config()
