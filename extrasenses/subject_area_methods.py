import random


class RandomForecast:
    """"Экземпляр класса при вызове метода get_forecast() возвращает случайное число от 0 до 100"""

    def get_forecast(self):
        return random.randint(0, 100)


class OnlyNewRandomForecast:
    """"Экземпляр класса при вызове метода get_forecast() возвращает случайное не повторяющееся число от 0 до 100"""

    def __init__(self):
        self.forecast_list = []

    def get_forecast(self):
        if len(self.forecast_list) < 100:
            forecast = random.randint(0, 100)
            if forecast not in self.forecast_list:
                self.forecast_list.append(forecast)
                return forecast
            else:
                self.get_forecast()
        else:
            self.forecast_list = []
            self.get_forecast()


class Extrasens:
    """Объект класса Extrasens принимает аргументами имя экстрасенса и не обязательный параметр -
    метод прогнозирования. По умолчанию используется метод случайного ответа. Метод объекта guess_number()
    возвращает прогноз, сформированный полученным методом или методом по умолчанию"""
    def __init__(self, name, forecast_method=None):
        self.name = name
        self._forecast_method = forecast_method or RandomForecast()

    def __str__(self):
        return self.name

    def guess_number(self):
        return self._forecast_method.get_forecast()

