import pandas as pd
import math

pd.set_option("display.max_columns", None)
df_currencies = pd.read_csv("currencies.csv")
data = {"name": [], "salary": [], "area_name": [], "published_at": []}
currencies = ['RUR', 'USD', 'KZT', 'BYR', 'UAH', 'EUR']
df = pd.read_csv("vacancies_dif_currencies.csv")


def get_name(row):
    return row['name']


def get_area_name(row):
    return row['area_name']


def get_published(row):
    return row['published_at']


def get_salary(row):
    salary_from = row["salary_from"]
    salary_to = row["salary_to"]
    salary_currency = row["salary_currency"]
    if (math.isnan(salary_from) and math.isnan(salary_to)) or salary_currency not in currencies:
        return None
    if salary_currency != 'RUR':
        date = row["published_at"][:7]
        k2 = df_currencies[df_currencies["date"] == date]
        k3 = k2[salary_currency].values
        try:
            k = float(k3)
        except:
            k = 0
    else:
        k = 1
    if math.isnan(salary_from):
        salary_from = salary_to
    if math.isnan(salary_to):
        salary_to = salary_from
    return ((salary_from + salary_to) / 2) * k


new_df = pd.DataFrame(data)
new_df['name'] = df['name']
new_df['area_name'] = df['area_name']
new_df['published_at'] = df['published_at']
new_df['salary'] = df.apply(get_salary, axis=1)

df_to_csv = new_df.head(100)
df_to_csv.to_csv("vacancies_100_2.csv")
