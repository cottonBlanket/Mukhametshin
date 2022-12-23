from unittest import TestCase
from task_3 import GraphData, Vacancy

vacancy_fields = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']
vacancy_row1 = ["Программист", 10000, 20000, "RUR", "Екатеринбург", "2022-12-03T22:39:07+0500"]
vacancy_row2 = ["Аналитик", 1000, 2000, "EUR", "Москва", "2021-12-03T22:39:07+0500"]
data_vacancies = [Vacancy(dict(zip(vacancy_fields, vacancy_row1))),
                      Vacancy(dict(zip(vacancy_fields, vacancy_row2)))]


class SalaryTest(TestCase):

    def test_convert_to_rub(self):
        self.assertEqual(data_vacancies[0].salary.convert_to_rub(), 15000)
        self.assertEqual(data_vacancies[1].salary.convert_to_rub(), 89850.0)


class CalculateDataByYears(TestCase):
    test_data = GraphData(data_vacancies, "years")

    def test_data_years(self):
        self.assertEqual(list(self.test_data.salary_data.keys()), [2022, 2021])
        self.assertEqual(list(self.test_data.count_data.keys()), [2022, 2021])

    def test_data_salary_by_years(self):
        self.assertEqual(self.test_data.salary_data[2022], 15000)

    def test_years_count(self):
        self.assertEqual(self.test_data.count_data[2021], 1)

    def test_years_len(self):
        self.assertEqual(len(self.test_data.salary_data), 2)
        self.assertEqual(len(self.test_data.count_data), 2)


class CalculateDataByAreas(TestCase):
    test_data = GraphData(data_vacancies, "areas")

    def test_data_areas(self):
        self.assertEqual(list(self.test_data.salary_data.keys()), ['Екатеринбург', 'Москва'])
        self.assertEqual(list(self.test_data.count_data.keys()), ['Екатеринбург', 'Москва'])

    def test_data_salary_by_areas(self):
        self.assertEqual(self.test_data.salary_data['Москва'], 89850)
        self.assertEqual(self.test_data.salary_data['Екатеринбург'], 15000)

    def test_data_count_by_areas(self):
        self.assertEqual(self.test_data.count_data['Москва'], 1)
        self.assertEqual(self.test_data.count_data['Екатеринбург'], 1)

    def test_data_len_by_areas(self):
        self.assertEqual(len(self.test_data.salary_data), 2)
        self.assertEqual(len(self.test_data.count_data), 2)

    def test_area_part(self):
        self.assertEqual(self.test_data.get_graph_data()[1]['Москва'], 0.5)
        self.assertEqual(self.test_data.get_graph_data()[1]['Екатеринбург'], 0.5)


class CalculateDataByProfAreas(TestCase):
    test_data = GraphData(data_vacancies, "areas", "Аналитик")

    def test_prof_areas(self):
        self.assertEqual(list(self.test_data.salary_data.keys()), ['Екатеринбург', 'Москва'])
        self.assertEqual(list(self.test_data.count_data.keys()), ['Екатеринбург', 'Москва'])

    def test_prof_count_by_areas(self):
        self.assertEqual(self.test_data.count_data['Москва'], 1)

    def test_prof_len_by_areas(self):
        self.assertEqual(len(self.test_data.salary_data), 2)
        self.assertEqual(len(self.test_data.count_data), 2)


class CalculateDataByProfYears(TestCase):
    test_data = GraphData(data_vacancies, "years", "Программист")

    def test_prof_years(self):
        self.assertEqual(list(self.test_data.salary_data.keys()), [2022, 2021])
        self.assertEqual(list(self.test_data.count_data.keys()), [2022, 2021])

    def test_prof_count_by_years(self):
        self.assertEqual(self.test_data.count_data[2022], 1)

    def test_prof_len_by_years(self):
        self.assertEqual(len(self.test_data.salary_data), 2)
        self.assertEqual(len(self.test_data.count_data), 2)

    def test_area_part_by_years(self):
        self.assertEqual(self.test_data.get_graph_data()[1][2022], 1)




