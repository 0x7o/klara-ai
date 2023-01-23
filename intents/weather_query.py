from fuzzywuzzy import fuzz
import requests
import json


class WeatherQuery:
    def __init__(self, config):
        self.url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = config.get_config("openweathermap_api_key")
        self.default_city = config.get_config("default_city")
        self.date = {
            tuple(["сегодня", "сейчас"]): "today",
            tuple(["завтра"]): "tomorrow",
            tuple(["послезавтра"]): "after_tomorrow",
        }
        self.weather_descriptor = {
            tuple(["солнечно"]): "clear",
            tuple(["облачно"]): "cloudy",
            tuple(["дождь"]): "rain",
            tuple(["снег"]): "snow",
            tuple(["гроза"]): "thunderstorm",
        }

    def get_weather(self, ner):
        # find and match B-place_name
        place_name = ""
        for entity in ner:
            if entity["entity"] == "B-place_name":
                place_name += entity["word"]

        # find and match B-date
        date = ""
        for entity in ner:
            if entity["entity"] == "B-date":
                date += entity["word"]

        for key in self.date.keys():
            if fuzz.ratio(date, key[0]) > 80:
                date = self.date[key]
            try:
                if fuzz.ratio(date, key[1]) > 80:
                    date = self.date[key]
            except IndexError:
                pass

        # find and match B-weather_descriptor
        weather_descriptor = ""
        for entity in ner:
            if entity["entity"] == "B-weather_descriptor":
                weather_descriptor += entity["word"]

        for key in self.weather_descriptor.keys():
            if fuzz.ratio(weather_descriptor, key[0]) > 80:
                weather_descriptor = self.weather_descriptor[key]

        # if no place_name, use default city
        if place_name == "":
            place_name = self.default_city

        # if no date, use today
        if date == "":
            date = "today"

        # get weather
        tts = ""
        params = {
            "q": place_name,
            "appid": self.api_key,
            "units": "metric",
            "lang": "ru",
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = json.loads(response.text)
            if date == "today":
                if weather_descriptor == "":
                    tts = f"Сейчас в городе {place_name} {data['weather'][0]['description']}, температура {data['main']['temp']} градусов"
                else:
                    if weather_descriptor == data["weather"][0]["main"].lower():
                        tts = f"Сейчас в городе {place_name} {data['weather'][0]['description']}, температура {data['main']['temp']} градусов"
                    else:
                        tts = f"Сейчас в городе {place_name} не {weather_descriptor}"
            elif date == "tomorrow":
                if weather_descriptor == "":
                    tts = f"Завтра в городе {place_name} {data['weather'][0]['description']}, температура {data['main']['temp']} градусов"
                else:
                    if weather_descriptor == data["weather"][0]["main"].lower():
                        tts = f"Завтра в городе {place_name} {data['weather'][0]['description']}, температура {data['main']['temp']} градусов"
                    else:
                        tts = f"Завтра в городе {place_name} не {weather_descriptor}"
            elif date == "after_tomorrow":
                if weather_descriptor == "":
                    tts = f"Послезавтра в городе {place_name} {data['weather'][0]['description']}, температура {data['main']['temp']} градусов"
                else:
                    if weather_descriptor == data["weather"][0]["main"].lower():
                        tts = f"Послезавтра в городе {place_name} {data['weather'][0]['description']}, температура {data['main']['temp']} градусов"
                    else:
                        tts = (
                            f"Послезавтра в городе {place_name} не {weather_descriptor}"
                        )
        else:
            tts = "Не могу найти погоду"

        return tts
