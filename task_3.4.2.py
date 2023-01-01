import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd


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
        self.df = pd.read_csv(self.file_name)
        self.df['published_at'] = self.df['published_at'].apply(lambda x: int(x[:4]))
        self.years = self.df['published_at'].unique()
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
        result_data = dict()
        for year in self.years:
            self.csv_year_parser(year, result_data)
        self.fill_data(result_data)

    def fill_data(self, data: dict):
        for year, value in data.items():
            self.result_data.salary_by_years[year] = value[0]
            self.result_data.count_by_years[year] = value[1]
            self.result_data.profession_salary[year] = value[2]
            self.result_data.profession_count[year] = value[3]

    def csv_year_parser(self, year: str, data: dict):
        this_df = self.df[self.df['published_at'] == year]
        df_vacancy = this_df[this_df["name"].str.contains(self.profession)]
        if df_vacancy.empty:
            data[year] = [this_df['salary'].mean(), len(this_df.index), 0, 0]
        else:
            data[year] = [this_df['salary'].mean(), len(this_df.index),
                          math.floor(df_vacancy['salary'].mean()), len(df_vacancy.index)]

    def csv_city_parser(self):
        total = len(self.df)
        self.df['count'] = self.df.groupby('area_name')['area_name'].transform('count')
        df_norm = self.df[self.df['count'] > 0.01 * total]
        df_area = df_norm.groupby('area_name', as_index=False)['salary'].mean().sort_values(by='salary', ascending=False)
        df_count = df_norm.groupby('area_name', as_index=False)['count'].mean().sort_values(by='count', ascending=False)
        cities = df_count['area_name'].unique()
        self.result_data.salary_by_cities = {city: 0 for city in cities}
        self.result_data.count_by_cities = {city: 0 for city in cities}
        for city in cities:
            self.result_data.salary_by_cities[city] = int(df_area[df_area['area_name'] == city]['salary'])
            self.result_data.count_by_cities[city] = round(int(df_count[df_count['area_name'] == city]['count']) / total, 4)


class PngReport:
    def __init__(self, years_salary: dict, years_count: dict,
                 prof_salary: dict, prof_count: dict,
                 areas_salary: dict, areas_count: dict):
        self.years_salary = years_salary
        self.years_count = years_count
        self.prof_salary = prof_salary
        self.prof_count = prof_count
        self.areas_salary = areas_salary
        self.areas_count = areas_count

    def get_salary_graph(self):
        fig = plt.figure()
        plt.rcParams.update({'font.size': 8})
        self.add_bar_subplot(fig, "Уровень зарплат по годам", 221, self.years_salary, "средняя з/п", "y",
                                     subplot_type="", prof_dict=self.prof_salary,
                                     x2_label=f'з/п Аналитик')
        self.add_bar_subplot(fig, "Количество вакансий по годам", 222, self.years_count, "Количество вакансий", "y",
                                     subplot_type="", prof_dict=self.prof_count,
                                     x2_label=f'Количество вакансий Аналитик')
        self.add_bar_subplot(fig, "Уровень зарплат по городам", 223, self.areas_salary, "уровень з/п", "x",
                                     subplot_type="horizontal")
        self.add_pie_sublot(fig, "Доля вакансий по городам", 224, self.areas_count)

        plt.tight_layout()
        plt.savefig("graph_3_4_2.pdf", dpi=300)

    @classmethod
    def add_bar_subplot(cls, fig: figure, title: str, width: int, full_dict: dict, x1_label: str,  axis, subplot_type="", prof_dict={}, x2_label=""):
        ax = fig.add_subplot(width)
        ax.set_title(title, fontsize=8)
        ax.tick_params(axis="both", labelsize=8)
        ax.grid(True, axis=axis)
        if subplot_type == "horizontal":
            ax.barh(list(full_dict.keys()), list(full_dict.values()), label=x1_label, align="center")
            ax.invert_yaxis()
        else:
            x_axis = range(len(full_dict.keys()))
            x1 = list(map(lambda x: float(x) - 0.2, x_axis))
            x2 = list(map(lambda x: float(x) + 0.2, x_axis))
            ax.bar(x1, list(full_dict.values()), width=0.4, label=x1_label)
            ax.bar(x2, list(prof_dict.values()), width=0.4, label=x2_label)
            ax.set_xticks(x_axis, list(full_dict.keys()), rotation="vertical")
        ax.legend(fontsize=8)

    @classmethod
    def add_pie_sublot(cls, fig: figure, title: str, width: int, data: dict):
        ax = fig.add_subplot(width)
        ax.set_title(title, fontsize=8)
        ax.tick_params(axis="both", labelsize=8)
        keys = list(data.keys())
        values = list(data.values())
        ax.pie(values, labels=keys)


if __name__ == '__main__':
    handler = MultiprocessorHandler()
    report = PngReport(handler.result_data.salary_by_years, handler.result_data.count_by_years,
                       handler.result_data.profession_salary, handler.result_data.profession_count,
                       handler.result_data.salary_by_cities, handler.result_data.count_by_cities)
    report.get_salary_graph()
