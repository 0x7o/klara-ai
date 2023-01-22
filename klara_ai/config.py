import os
import json
import pyaudio


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            self.create_config()
            return self.load_config()

    def get_config(self, key):
        try:
            return self.config[key]
        except KeyError:
            assert False, f"Key {key} not found in config"

    def edit_config(self, key, value):
        self.config[key] = value
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def create_config(self):
        default_config = {
            "model_path": "vosk-model-small-ru-0.22",
            "sample_rate": 16000,
            "format": pyaudio.paInt16,
            "channels": 1,
            "frames_per_buffer": 8000,
            "endpoint_url": "http://localhost:8000",
            "device_index": 1,
            "bot_name": "Klara",
            "bot_language": "ru",
            "base_prompt": "This is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n",
            "history_file": "history.json",
            "openai_api_key": "YOUR_OPENAI_API_KEY",
            "sounds": {
                "start": "sounds/start.wav",
                "end": "sounds/end.wav",
                "error": "sounds/error.wav",
            },
        }
        with open(self.config_file, "w") as f:
            json.dump(default_config, f, indent=4)


if __name__ == "__main__":
    config = Config("config.json")
    print(config.get_config("model_path"))
