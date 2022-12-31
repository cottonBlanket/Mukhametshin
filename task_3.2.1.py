import csv


class DataSeparator:
    """
    Класс для разделения csv-файла на чанки по годам публикации вакансии
    :param file_name: имя файла для парсинга
    :type file_name: str
    :param fields: поля csv-файла
    :type fields: list
    :param data: данные csv-файла
    :type data: list
    """
    def __init__(self, file_name):
        """
        Инициализирует объект класса DataSeparator
        :param file_name: имя файла для парсинга
        :type file_name: str
        """
        self.file_name = file_name
        self.fields = []
        self.data = []

    def read_file(self):
        """
        Считывает файл для парсинга, убирает невалидные строки, определяет поля и данные файла
        :return: заполненные массивы полей и данных файла
        """
        with open(self.file_name, "r", encoding="utf-8-sig") as data:
            reader = csv.reader(data)
            self.fields = reader.__next__()
            self.data = [row for row in reader if not ("" in row) and len(row) == len(self.fields)]

    def create_csv(self, year: str, data: list):
        """
        Создает csv-файл с данными по году
        :param year: год
        :type year: str
        :param data: данные для записи в csv-файл
        :type data: list
        :return: созданный csv-файл
        """
        with open(f"DataSet/vacancies_by_{year}.csv", "a", encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(self.fields)
            writer.writerows(data)

    def csv_separate(self):
        """
        Разделяет csv-файл на части в зависимости от года
        :return: Созданы csv-файлы для каждого года
        """
        year = self.data[0][self.fields.index('published_at')][:4]
        data_by_year = []
        for vacancy in self.data:
            vacancy_year = vacancy[self.fields.index('published_at')][:4]
            if vacancy_year != year:
                self.create_csv(year, data_by_year)
                year = vacancy_year
                data_by_year = []
            data_by_year.append(vacancy)
        self.create_csv(year, data_by_year)


separator = DataSeparator("vacancies_by_year.csv")
separator.read_file()
separator.csv_separate()

