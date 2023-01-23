from num2words import num2words
import datetime


class DateTimeQuery:
    def __init__(self, config):
        self.config = config

    def get_time(self):
        now = datetime.datetime.now()
        hours = self.convert_temp(now.hour)
        minutes = self.convert_temp(now.minute)
        return f"Сейчас {hours} часов {minutes} минут"

    def convert_temp(self, number):
        return num2words(number, to="cardinal", lang="ru")
