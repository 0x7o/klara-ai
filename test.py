from klara_ai import Config, STT, Sound, OpenAI, Endpoint, pixels
from intents import *
import sounddevice as sd
import soundfile as sf
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
                    tts = weather.get_weather(ner)
                    wav = endpoint.tts_request(tts)
                    with open("temp.wav", "wb") as f:
                        f.write(wav)
                    pix.speak()
                    data, fs = sf.read("temp.wav", dtype="float32")
                    sd.play(data, fs)
                    status = sd.wait()
                    pix.off()
                    openai.write_history(tts, text)
                elif intent == "datetime_query":
                    datetime = DateTimeQuery(config)
                    tts = datetime.get_time(ner)
                    wav = endpoint.tts_request(tts)
                    with open("temp.wav", "wb") as f:
                        f.write(wav)
                    pix.speak()
                    data, fs = sf.read("temp.wav", dtype="float32")
                    sd.play(data, fs)
                    status = sd.wait()
                    pix.off()
                else:
                    try:
                        tts = openai.get_response(text)
                    except:
                        tts = "Я куку"
                    wav = endpoint.tts_request(tts)
                    with open("temp.wav", "wb") as f:
                        f.write(wav)
                    pix.speak()
                    data, fs = sf.read("temp.wav", dtype="float32")
                    sd.play(data, fs)
                    status = sd.wait()
                    pix.off()
                pix.listen()
            else:
                is_listening = False
                pix.off()
