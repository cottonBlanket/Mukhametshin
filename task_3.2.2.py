import cProfile
import math
import os.path
import pandas as pd
import multiprocessing


class Data:
    def __init__(self):
        self.salary_by_years = dict()
        self.count_by_years = dict()
        self.profession_salary = dict()
        self.profession_count = dict()
        self.salary_by_cities = dict()
        self.count_by_cities = dict()

    def sorted_dicts(self):
        self.salary_by_years = dict(sorted(self.salary_by_years.items(), key=lambda x: x[0], reverse=False))
        self.count_by_years = dict(sorted(self.count_by_years.items(), key=lambda x: x[0], reverse=False))
        self.profession_salary = dict(sorted(self.profession_salary.items(), key=lambda x: x[0], reverse=False))
        self.profession_count = dict(sorted(self.profession_count.items(), key=lambda x: x[0], reverse=False))
        self.salary_by_cities = dict(sorted(self.salary_by_cities.items(), key=lambda x: x[1], reverse=True))
        self.count_by_cities = dict(sorted(self.count_by_cities.items(), key=lambda x: x[1], reverse=True))


class MultiprocessorHandler:
    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.profession = input("Введите название профессии: ")
        self.result_data = Data()
        self.data = pd.read_csv("vacancies_by_year.csv")
        self.data['published_at'] = self.data['published_at'].apply(lambda x: int(x[:4]))
        self.years = self.data['published_at'].unique()
        self.data['salary'] = self.data[['salary_from', 'salary_to']].mean(axis=1)
        self.create_processes()
        self.csv_city_parser()
        self.result_data.sorted_dicts()

    def print_result(self):
        print('Динамика уровня зарплат по годам:', self.result_data.salary_by_years)
        print('Динамика количества вакансий по годам:', self.result_data.count_by_years)
        print('Динамика уровня зарплат по годам для выбранной профессии:', self.result_data.profession_salary)
        print('Динамика количества вакансий по годам для выбранной профессии:', self.result_data.profession_count)
        print('Уровень зарплат по городам (в порядке убывания):', self.result_data.salary_by_cities)
        print('Доля вакансий по городам (в порядке убывания):', self.result_data.count_by_cities)

    def create_processes(self):
        manager = multiprocessing.Manager()
        result_data = manager.dict()
        all_processes = []

        for year in self.years: 
            process = multiprocessing.Process(target=self.csv_year_parser, args=(year, result_data))
            all_processes.append(process)
            process.start()

        for process in all_processes:
            process.join()

        self.fill_data(result_data)

    def fill_data(self, data: dict):
        for year, value in data.items():
            self.result_data.salary_by_years[year] = value[0]
            self.result_data.count_by_years[year] = value[1]
            self.result_data.profession_salary[year] = value[2]
            self.result_data.profession_count[year] = value[3]

    def csv_year_parser(self, year: str, data: dict):
        file_name = rf"DataSet/vacancies_by_{year}.csv"
        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            df['salary'] = df[["salary_from", "salary_to"]].mean(axis=1)
            df_vacancy = df[df["name"].str.contains(self.profession)]
            if df_vacancy.empty:
                data[year] = [df['salary'].mean(), len(df.index), 0, 0]
            else:
                data[year] = [df['salary'].mean(), len(df.index),
                              math.floor(df_vacancy['salary'].mean()), len(df_vacancy.index)]

    def csv_city_parser(self):
        total = len(self.data)
        self.data['count'] = self.data.groupby('area_name')['area_name'].transform('count')
        df_norm = self.data[self.data['count'] > 0.01 * total]
        df_area = df_norm.groupby('area_name', as_index=False)['salary'].mean().sort_values(by='salary', ascending=False)
        df_count = df_norm.groupby('area_name', as_index=False)['count'].mean().sort_values(by='count', ascending=False)
        cities = df_count['area_name'].unique()
        self.result_data.salary_by_cities = {city: 0 for city in cities}
        self.result_data.count_by_cities = {city: 0 for city in cities}
        for city in cities:
            self.result_data.salary_by_cities[city] = int(df_area[df_area['area_name'] == city]['salary'])
            self.result_data.count_by_cities[city] = round(int(df_count[df_count['area_name'] == city]['count']) / total, 4)


if __name__ == '__main__':
    cProfile.run('MultiprocessorHandler().print_result()')
