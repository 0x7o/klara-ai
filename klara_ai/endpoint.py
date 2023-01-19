from config import Config
import requests


class Endpoint:
    def __init__(self, config: Config):
        self.config = config

    def stt_request(self, base64_string):
        url = self.config.get_config('endpoint_url') + '/stt'
        headers = {'Content-Type': 'application/json'}
        data = {'audio': base64_string}
        response = requests.post(url, headers=headers, json=data)
        return response.json()
  