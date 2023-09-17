

import requests
from bs4 import BeautifulSoup
import fake_headers
import lxml



keywords = ['дизайн', 'фото', 'web', 'python']
heders_gen = fake_headers.Headers(browser='firefox', os='win')

response = requests.get('https://habr.com/ru/articles/', headers=heders_gen.generate())

html_data = response.text

sour = BeautifulSoup(html_data, 'lxml')
articles_list = sour.find('div', class_='tm-articles-list')
articles_tags = articles_list.find_all('article')

article_post = []


for articles_tag in articles_tags:
    heder_tag = articles_tag.find('h2')
    a_tag = heder_tag.find('a')
    heder_text = heder_tag.text
    link = a_tag['href']
    link = f'https://habr.com{link}'
    data_tag = articles_tag.find('time')
    time_publication = data_tag['datetime']

    for el in keywords:
        post = {}
        if el in articles_tag.text:
            post['time'] = time_publication
            post['heder'] = heder_text
            post['link'] = link
            article_post.append(post)
print(article_post)








