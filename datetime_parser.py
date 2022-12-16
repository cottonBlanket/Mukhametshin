import datetime as dt
import dateparser
import cProfile
from profile import Profile


class DateTimeParser:
    """
    Класс для парсинга строки даты и времени

    :param datetime: полная строка даты и времени
    :type datetime: str
    """
    def __init__(self, str_datetime: str):
        """
        Инициализирует объект класса DateTimeParser
        :param str_datetime: полная строка даты и времени
        :type str_datetime: str
        """
        self.datetime = str_datetime

    def get_year_by_datetime(self):
        """
        Функция для получения года с помощью класса datetime
        :return: Год
        :rtype: int
        """
        format = '%Y-%m-%dT%H:%M:%S%z'
        return dt.datetime.strptime(self.datetime, format).year

    def get_year_by_split_parser(self):
        """
        Функция для получения года с помощью метода split
        :return: Год
        :rtype: str
        """
        return self.datetime.split('-')[0]

    def get_year_by_str_index(self):
        """
        Функция для получения года с помощью индексации строк
        :return: Год
        :rtype: str
        """
        return self.datetime[:4]

    def get_year_by_dateparser(self):
        """
        Функция для получения года с помощью класса dateparser
        :return: Год
        :rtype: int
        """
        return dateparser.parse(self.datetime).year



