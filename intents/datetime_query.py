import translators.server as ts
from num2words import num2words
from datetime import datetime
import pytz


class DateTimeQuery:
    def __init__(self, config):
        self.config = config

    def get_time(self, ner):
        place_name = ""
        for entity in ner:
            if entity["entity"] == "B-place_name":
                place_name += entity["word"]

        if place_name == "":
            place_name = self.config.get_config("default_city")
        try:
            timezone = pytz.timezone(
                ts.google(place_name, from_language="ru", to_language="en")
            )
        except:
            timezone = pytz.timezone("Europe/Moscow")
        time = datetime.now(timezone)
        hour = self.convert_temp(time.hour)
        minute = self.convert_temp(time.minute)
        return f"Сейчас в {place_name} {hour} часов {minute} минут"

    def convert_temp(self, number):
        return num2words(number, to="cardinal", lang="ru")
