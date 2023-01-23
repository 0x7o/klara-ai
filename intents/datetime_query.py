from num2words import num2words
import datetime
import requests


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

    def convert_temp(self, number):
        return num2words(number, to="cardinal", lang="ru")
