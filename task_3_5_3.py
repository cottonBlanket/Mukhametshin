import csv, math
import sqlite3
import pandas as pd


class SQLReport:
    """Класс для создания 6-ти запросов в базу данных.
    Attributes:
        dbName (str): имя базы данных с вакансиями.
        prof (str): название професии.
    """

    def __init__(self, dbName: str, prof: str):
        """Инициализация. Создание всех запросов и вывод результата на экран.
        Args:
            dbName (str): имя базы данных с вакансиями.
            prof (str): название професии.
        """
        self.connect = sqlite3.connect(dbName)
        self.printSalaryByYear()
        self.printCountByYear()
        self.printSalaryByYearForVacancy(prof)
        self.printCountByYearForVacancy(prof)
        self.printSalaryByArea()
        self.printPieceByArea()

    def printSalaryByYear(self) -> None:
        """Создает запрос по средней зарплате всех вакансий по годам"""
        print("Динамика уровня зарплат по годам")
        sqlQuery = """
            SELECT strftime('%Y', published_at) as year, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary
            FROM task_3_5_2 
            GROUP BY strftime('%Y', published_at);
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def printCountByYear(self) -> None:
        """Создает запрос по количеству всех вакансий по годам"""
        print("Динамика количества вакансий по годам")
        sqlQuery = """
            SELECT strftime('%Y', published_at) as year, COUNT(*) as count
            FROM task_3_5_2 
            GROUP BY strftime('%Y', published_at);
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def printSalaryByYearForVacancy(self, prof: str) -> None:
        """Создает запрос по средней зарплате нужных вакансий по годам"""
        print("Динамика уровня зарплат по годам для выбранной профессии")
        sqlQuery = f" \
            SELECT strftime('%Y', published_at) as year, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary \
            FROM task_3_5_2 \
            WHERE name LIKE '%{prof}%' \
            GROUP BY strftime('%Y', published_at); \
        "
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def printCountByYearForVacancy(self, prof: str) -> None:
        """Создает запрос по количеству нужных вакансий по годам"""
        print("Динамика количества вакансий по годам для выбранной профессии")
        sqlQuery = f" \
            SELECT strftime('%Y', published_at) as year, COUNT(*) as count \
            FROM task_3_5_2 \
            WHERE name LIKE '%{prof}%' \
            GROUP BY strftime('%Y', published_at); \
        "
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def printSalaryByArea(self) -> None:
        """Создает запрос по средней зарплате в городах."""
        print("Уровень зарплат по городам")
        sqlQuery = """
            SELECT area_name, COUNT(*) as count, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary
            FROM task_3_5_2 
            GROUP BY area_name 
            HAVING count > (SELECT COUNT(*) FROM task_3_5_2) / 100
            ORDER BY avg_salary DESC
            LIMIT 10;
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def printPieceByArea(self) -> None:
        """Создает запрос по доле городов."""
        print("Доля вакансий по городам")
        sqlQuery = """
            SELECT area_name, COUNT(*) as count, 
                CAST(ROUND(CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM task_3_5_2) * 100, 4) AS VARCHAR) || '%' AS piece
            FROM task_3_5_2 
            GROUP BY area_name 
            HAVING count > (SELECT COUNT(*) FROM task_3_5_2) / 100
            ORDER BY COUNT(*) DESC
            LIMIT 10;
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()


def setPandasOptions():
    """Устанавливает настройки pandas, чтобы корректно отображать класс DataFrame в консоли."""
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.expand_frame_repr', False)


if __name__ == '__main__':
    setPandasOptions()
    fileName = "Database_3_5_1.db"
    professionName = "Программист"
    input_values = SQLReport(fileName, professionName)