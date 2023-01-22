from klara_ai import Pixels, STT, Sound, OpenAI, Config, Endpoint

config = Config("config.json")
pixels = Pixels(config)
stt = STT(config)
sound = Sound(config)
openai = OpenAI(config)
endpoint = Endpoint(config)

if __name__ == "__main__":
    sound.play("start")