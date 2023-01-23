from klara_ai import Config, STT, Sound, OpenAI, Endpoint, pixels
from intents import *
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
pix = pixels.Pixels()

if __name__ == "__main__":
    pix.wakeup()
    pix.off()
    is_listening = False
    while True:
        if not is_listening:
            text = stt.listen(process=False)
            if "клара" in text:
                pix.listen()
                is_listening = True
        else:
            text = stt.listen()
            if text != "":
                print(text)
                pix.think()
                intent = endpoint.intent_request(text)
                print(intent)

                ner = endpoint.ner_request(text)
                if intent == "weather_query":
                    weather = WeatherQuery(config)
                    print(weather.get_weather(ner))
                pix.listen()
            else:
                is_listening = False
                pix.off()
