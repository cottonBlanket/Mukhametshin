import csv
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


class Salary:
    currency_to_rub = {"AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76, "KZT": 0.13, "RUR": 1,
                       "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}

    def __init__(self, salary_from, salary_to, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency

    def convert_to_rub(self) -> float:
        value = float(self.currency_to_rub[self.salary_currency])
        return ((float(self.salary_from) + float(self.salary_to)) / 2) * value


class Vacancy:
    def __init__(self, vacancy_dict):
        self.dict = vacancy_dict
        self.salary = Salary(self.dict['salary_from'], self.dict['salary_to'], self.dict['salary_currency'])


class Input:
    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.profession = input("Введите название профессии: ")
        self.fields = []

    def csv_parser(self):
        reader = self.csv_reader(self.file_name)
        data_all_vacancies = []
        for row in reader:
            new_vacancy = self.get_vacancy(row)
            data_all_vacancies.append(new_vacancy)
        return data_all_vacancies

    def csv_reader(self, file_name) -> []:
        with open(file_name, encoding="utf-8-sig") as test:
            unpacker = csv.reader(test)
            data = []
            length = 0
            for row in unpacker:
                if length < len(row):
                    length = len(row)
                if '' not in row and length == len(row):
                    data.append(row)
            self.fields = data[0]
            return data[1:]

    def get_vacancy(self, row: []) -> Vacancy:
        vacancy = Vacancy(dict(zip(self.fields, row)))
        return vacancy


class GraphData:
    def __init__(self, data, x_axis, profession="not"):
        self.data = data
        self.profession = profession
        self.salary_data = dict()
        self.count_data = dict()
        self.calculate_data(x_axis)
        self.x_axis = x_axis

    def calculate_data(self, x_axis):
        for vacancy in self.data:
            self.add_data_from_vacancy(vacancy, x_axis)
        for x in self.salary_data:
            if self.count_data[x] != 0:
                self.salary_data[x] = math.floor(self.salary_data[x] / self.count_data[x])

    def add_data_from_vacancy(self, vacancy: Vacancy, x_axis):
        if x_axis == "years":
            abscissa = int(vacancy.dict['published_at'].split('-')[0])
        else:
            abscissa = vacancy.dict['area_name']
        if abscissa not in self.salary_data:
            self.salary_data[abscissa] = 0
        if abscissa not in self.count_data:
            self.count_data[abscissa] = 0
        salary = vacancy.salary.convert_to_rub()
        if self.profession != "not" and self.profession not in vacancy.dict['name']:
            return
        self.update_dicts(abscissa, salary)

    def update_dicts(self, key: str, value: float):
        try:
            self.salary_data[key] += value
            self.count_data[key] += 1
        except:
            self.salary_data[key] = value
            self.count_data[key] = 1

    def get_graph_data(self):
        first_printed_dict = self.salary_data
        second_printed_dict = self.count_data
        if self.x_axis == "areas":
            vac_count = sum(list(second_printed_dict.values()))
            first_printed_dict = self.sorted_dict(dict(list(filter(lambda x: self.count_data[x[0]] / vac_count > 0.01, self.salary_data.items()))))
            second_printed_dict = self.sorted_dict(dict(list(filter(lambda x: self.count_data[x[0]] / vac_count > 0.01, self.count_data.items()))))
            for x in second_printed_dict:
                second_printed_dict[x] = float("%.4f" % (second_printed_dict[x] / vac_count))
        return first_printed_dict, second_printed_dict

    @classmethod
    def sorted_dict(cls, non_sorted_dict: dict) -> dict:
        return dict(list(sorted(non_sorted_dict.items(), key=lambda x: x[1], reverse=True))[:10])


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
                                     x2_label=f'з/п {input_set.profession}')
        self.add_bar_subplot(fig, "Количество вакансий по годам", 222, self.years_count, "Количество вакансий", "y",
                                     subplot_type="", prof_dict=self.prof_count,
                                     x2_label=f'Количество вакансий {input_set.profession}')
        self.add_bar_subplot(fig, "Уровень зарплат по городам", 223, self.areas_salary, "уровень з/п", "x",
                                     subplot_type="horizontal")
        self.add_pie_sublot(fig, "Доля вакансий по городам", 224, self.areas_count)

        plt.tight_layout()
        plt.savefig("graph.png", dpi=300)

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


input_set = Input()
years = GraphData(input_set.csv_parser(), "years")
prof_years = GraphData(input_set.csv_parser(), "years", input_set.profession)
areas = GraphData(input_set.csv_parser(), "areas")
dicts = [years.get_graph_data()[0], years.get_graph_data()[1],
                             prof_years.get_graph_data()[0], prof_years.get_graph_data()[1],
                             areas.get_graph_data()[0], areas.get_graph_data()[1]]
png = PngReport(dicts[0], dicts[1], dicts[2], dicts[3], dicts[4], dicts[5])
png.get_salary_graph()

