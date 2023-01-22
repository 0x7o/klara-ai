from config import Config
import pyaudio
import wave


class Sounds:
    def __init__(self, config: Config):
        self.config = config
        self.p = pyaudio.PyAudio()

    def play(self, sound):
        wf = wave.open(self.config.get_config("sounds")[sound], "rb")
        stream = self.p.open(
            format=self.p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            output_device_index=self.config.get_config("device_index"),
        )
        data = wf.readframes(1024)
        while data != b"":
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()

    def close(self):
        self.p.terminate()


if __name__ == "__main__":
    config = Config("config.json")
    sounds = Sounds(config)
    sounds.play("start")
    sounds.close()
