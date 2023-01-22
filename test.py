from klara_ai import Config, STT, Sound, OpenAI, Endpoint, pixels
import logging
import time

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
pix = pixels.Pixels()

if __name__ == "__main__":
    pix.wakeup()
    pix.off()
    is_listening = False
    while True:
        if not is_listening:
            text = stt.listen(process=False)
            print(text)
            if "клара" in text:
                pix.listen()
                is_listening = True
                if len(text) > 1:
                    pix.think()
                    time.sleep(1)
                    pix.off()
        else:
            text = stt.listen()
            if text != "":
                print(text)
            else:
                is_listening = False
                pix.think()
                time.sleep(1)
                pix.off()
