import pandas as pd
import math

pd.set_option("display.max_columns", None)
df_currencies = pd.read_csv("currencies.csv")
df = pd.read_csv("vacancies_dif_currencies.csv")
currencies = ['RUR', 'USD', 'KZT', 'BYR', 'UAH', 'EUR']
new_df = {"name": [], "salary": [], "area_name": [], "published_at": []}


def find_coefficient(currency, line):
    if currency != 'RUR':
        date = line["published_at"][:7]
        return float(df_currencies[df_currencies["date"] == date][currency].values)
    return 1


def find_salary(salary_start, salary_end, coefficient):
    if math.isnan(salary_start):
        salary_start = salary_end
    if math.isnan(salary_end):
        salary_end = salary_start
    return ((salary_start + salary_end) / 2) * coefficient


for index, row in df.iterrows():
    if len(new_df['name']) > 100:
        break
    salary_from = row["salary_from"]
    salary_to = row["salary_to"]
    salary_currency = row["salary_currency"]
    if (math.isnan(salary_from) and math.isnan(salary_to)) or salary_currency not in currencies:
        continue
    new_df["salary"].append(find_salary(salary_from, salary_to, find_coefficient(salary_currency, row)))
    new_df["name"].append(row["name"])
    new_df["area_name"].append(row["area_name"])
    new_df["published_at"].append(row["published_at"])

new_df = pd.DataFrame(new_df)
new_df.to_csv("vacancies_100.csv")
