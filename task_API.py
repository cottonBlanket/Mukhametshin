from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from dateutil import rrule
import pandas as pd

pd.set_option("display.max_columns", None)
file = "vacancies_dif_currencies.csv"
df = pd.read_csv(file)
currencies_df = df['salary_currency']


class Currency:
    def __init__(self, currencies_data):
        self.currencies_data = currencies_data
        self.currencies_frequency = dict()
        self.popular_currencies = dict()
        self.calculate_frequency()
        self.calculate_popular_currencies()

    def calculate_frequency(self):
        for x in self.currencies_data:
            try:
                self.currencies_frequency[x] += 1
            except:
                self.currencies_frequency[x] = 1

    def calculate_popular_currencies(self):
        for x in self.currencies_frequency:
            if str(x) != 'nan' and self.currencies_frequency[x] > 5000:
                self.popular_currencies[x] = []
        self.popular_currencies['date'] = []
        self.popular_currencies.pop('RUR')

    def print_currencies(self):
        for x in self.currencies_frequency:
            print(f'{x}: {self.currencies_frequency[x]}')


currencies = Currency(currencies_df).popular_currencies

min_date = datetime.strptime(df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z')
max_date = datetime.strptime(df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z')
for dt in rrule.rrule(rrule.MONTHLY, dtstart=min_date, until=max_date):
    tree = ET.parse(urlopen(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{dt.strftime("%m/%Y")}d=1'))
    root = tree.getroot()
    for child in root.findall('Valute'):
        code = child.find('CharCode').text
        a = currencies.keys()
        if code in currencies.keys():
            if dt.strftime('%Y-%m') not in currencies['date']:
                currencies['date'] += [dt.strftime('%Y-%m')]
            k = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
            currencies[code].append(k)
            print(code == 'BYR')
    if len(currencies['BYR']) != len(currencies['date']):
        currencies['BYR'].append(None)
new_df = pd.DataFrame(currencies)
new_df.to_csv('currencies.csv')
