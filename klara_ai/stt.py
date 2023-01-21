from vosk import Model, KaldiRecognizer
from endpoint import Endpoint
from config import Config
import sounddevice as sd
import soundfile as sf
import numpy as np
import pyaudio
import base64
import json


class STT:
    def __init__(self, config: Config, endpoint: Endpoint):
        self.config = config
        try:
            self.model = Model(self.config.get_config("model_path"))
        except:
            assert (
                False
            ), f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{self.config.get_config('model_path')}' in the current folder."
        self.rec = KaldiRecognizer(self.model, self.config.get_config("sample_rate"))
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.config.get_config("format"),
            channels=self.config.get_config("channels"),
            rate=self.config.get_config("sample_rate"),
            input=True,
            frames_per_buffer=self.config.get_config("frames_per_buffer"),
            input_device_index=self.config.get_config("device_index"),
        )
        self.stream.start_stream()
        self.wav = []
        self.endpoint = endpoint

    def listen(self):
        c = 0
        while True:
            data = self.stream.read(
                self.config.get_config("frames_per_buffer"), exception_on_overflow=False
            )
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                self.wav.append(data)
                print(self.rec.Result())
                try:
                    text = json.loads(self.rec.Result())
                except:
                    text = {"text": ""}
                if text["text"] != "":
                    wav = np.frombuffer(b"".join(self.wav), dtype=np.int16)
                    base64_bytes = base64.b64encode(wav)
                    base64_string = base64_bytes.decode("utf-8")
                    print("* decoding")
                    response = self.endpoint.stt_request(base64_string)
                    self.wav = []
                    c = 0
                    return response
                else:
                    c += 1
                    if c > 2:
                        self.wav = []
                        return ""
            else:
                self.wav.append(data)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == "__main__":
    config = Config("config.json")
    endpoint = Endpoint(config)
    stt = STT(config, endpoint)
    while True:
        text = stt.listen()
        # tts
        if text != "":
            print(text)
            wav = endpoint.tts_request(text)
            print("* playing")
            # save to temp file
            with open("temp.wav", "wb") as f:
                f.write(wav)
            # play
            data, fs = sf.read("temp.wav", dtype="float32")
            sd.play(data, fs)
            status = sd.wait()
