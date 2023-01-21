from config import Config
import requests
import base64


class Endpoint:
    def __init__(self, config: Config):
        self.config = config

    def stt_request(self, base64_string):
        url = self.config.get_config("endpoint_url") + "/stt"
        headers = {"Content-Type": "application/json"}
        data = {"audio": base64_string}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def tts_request(self, text):
        url = self.config.get_config("endpoint_url") + "/tts"
        headers = {"Content-Type": "application/json"}
        data = {"text": text}
        response = requests.post(url, headers=headers, json=data)
        base64_string = response.json()["audio"]
        # decoding to wav file
        base64_bytes = base64_string.encode("utf-8")
        wav = base64.b64decode(base64_bytes)
        return wav

    def translate_request(
        self, text, src_lang, tgt_lang, gender_name, gender_translation
    ):
        url = self.config.get_config("endpoint_url") + "/nllb"
        headers = {"Content-Type": "application/json"}
        data = {
            "text": text,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang,
            "gender_name": gender_name,
            "gender_translation": gender_translation,
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
