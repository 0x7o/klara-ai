from klara_ai import Config, STT, Sound, OpenAI, Endpoint
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="klara.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


config = Config("config.json")
endpoint = Endpoint(config)
stt = STT(config, endpoint)
sound = Sound(config)
openai = OpenAI(config)

if __name__ == "__main__":
    sound.play("start")
    is_listening = False
    while True:
        if not is_listening:
            text = stt.listen(process=False)
            print(text)
            if "клара" in text:
                sound.play("start")
                is_listening = True
        else:
            text = stt.listen()
            if text != "":
                print(text)
            else:
                is_listening = False
                sound.play("end")
