import json

import requests
from bs4 import BeautifulSoup
import fake_headers
from pprint import pprint



keywords = ['Django', 'Flask']
heders_gen = fake_headers.Headers(browser='firefox', os='win')

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=heders_gen.generate())

html_data = response.text

sour = BeautifulSoup(html_data, 'lxml')
articles_list = sour.find('div', {'data-qa': 'vacancy-serp__results'})
articles_tags = articles_list.find_all('div', class_='serp-item')

job_list = {}
index_job = 1
for articles_tag in articles_tags:
    heder_tag = articles_tag.find('h3')

    company_tag = articles_tag.find('div', class_='vacancy-serp-item-company')
    company = company_tag.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company_name = company.text

    salary_tag = articles_tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary_tag == None:
        salary_text = 'Зарплата не указана'
    else:
        salary_text = salary_tag.text

    city = company_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city_text = city.text

    a_tag = heder_tag.find('a')
    link = a_tag['href']

    response = requests.get(link, headers=heders_gen.generate())
    html_data_post = response.text
    sour_post = BeautifulSoup(html_data_post, 'lxml')
    content = sour_post.find('div', class_='g-user-content')

    for el in keywords:
        vacancy = {}
        if el in content.text:
            vacancy['link'] = link
            vacancy['salary'] = salary_text
            vacancy['company_name'] = company_name
            vacancy['city'] = city_text
            job_list[index_job] = vacancy
            index_job += 1
pprint(job_list)


with open('jobs_list.json', 'w', encoding='utf-8') as f:
    json.dump(job_list, f, ensure_ascii=False)




