import pandas as pd
import requests
import json

pd.set_option("display.max_columns", None)
data = {'name': [], 'salary_from': [], 'salary_to': [], 'salary_currency': [], 'area_name': [], 'published_at': []}
date = ['2022-12-23T00:00:00', '2022-12-23T06:00:00', '2022-12-23T12:00:00', '2022-12-23T18:00:00', '2022-12-24T00:00:00']

for k in range(len(date) - 1):
    date_from = date[k]
    date_to = date[k+1]
    for j in range(1, 20):
        request = requests.get(
            f'https://api.hh.ru/vacancies?date_from={date_from}&date_to={date_to}&specialization=1&per_page=100&page={j}')
        jsonText = request.text
        jsonData = json.loads(jsonText)
        items = jsonData['items']
        if len(items) == 0:
            break
        for i in items:
            data['name'].append(i['name'])
            salary = i['salary']
            if salary != None:
                data['salary_from'].append(salary['from'])
                data['salary_to'].append(salary['to'])
                data['salary_currency'].append(salary['currency'])
            else:
                data['salary_from'].append(None)
                data['salary_to'].append(None)
                data['salary_currency'].append(None)
            area = i['area']
            if area != None:
                data['area_name'].append(area['name'])
            else:
                data['area_name'].append(None)
            data['published_at'].append(i['published_at'])

df = pd.DataFrame(data)
df.to_csv('hh.csv')
