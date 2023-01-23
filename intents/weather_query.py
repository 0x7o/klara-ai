from num2words import num2words
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
            tts = self.get_weather_tts(data, date)
        else:
            tts = f"Не могу получить погоду в {place_name}."

        return tts

    def get_weather_tts(self, data, date):
        tts = ""
        if date == "today":
            tts += f"Сейчас в {data['name']} {self.convert_temp_to_words(data['main']['temp'])} градусов, {data['weather'][0]['description']}."
            tts += f" Днём ожидается {self.convert_temp_to_words(data['main']['temp_max'])}, а ночью {self.convert_temp_to_words(data['main']['temp_min'])}."
        elif date == "tomorrow":
            tts += f"Завтра в {data['name']} {self.convert_temp_to_words(data['main']['temp'])} градусов, {data['weather'][0]['description']}."
        elif date == "after_tomorrow":
            tts += f"Послезавтра в {data['name']} {self.convert_temp_to_words(data['main']['temp'])} градусов, {data['weather'][0]['description']}."
        else:
            tts += f"Не могу предсказать погоду на {date}."
        return tts

    def convert_temp_to_words(temp):
        return num2words(temp, to="cardinal", lang="ru")
