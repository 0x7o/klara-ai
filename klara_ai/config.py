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
            "sample_rate": 8000,
            "format": pyaudio.paInt16,
            "channels": 2,
            "frames_per_buffer": 4000,
            "endpoint_url": "http://localhost:8000",
        }
        with open(self.config_file, "w") as f:
            json.dump(default_config, f, indent=4)


if __name__ == "__main__":
    config = Config("config.json")
    print(config.get_config("model_path"))
