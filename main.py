import requests
from pprint import pprint
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


def get_headers():
    return Headers(browser='firefox', os='win').generate()


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
hh_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_html, features='lxml')
vacancies = soup.find(id='a11y-main-content')
vacancy = vacancies.find_all(class_='serp-item')

vacancy_description = []
for item in vacancy:
    description = item.find(class_='vacancy-serp-item__layout')
    description_text = description.find(class_='g-user-content').text
    if 'Django' in description_text and 'Flask' in description_text:
        vacancy_description.append(item)


vacancy_list = []
for word in vacancy_description:
    title = word.find('a', class_='serp-item__title').text
    link_tag = word.find('a', class_='serp-item__title')
    link = link_tag['href']
    try:
        salary_tag = word.find('span', class_='bloko-header-section-3')
        salary = salary_tag.text
    except Exception:
        salary = 'Не указана'
    company_tag = word.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company = company_tag.text
    city_tag = word.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'})
    city = city_tag.text

    vacancy_list.append({
        'Вакансия': title,
        'Ссылка': link,
        'Зарплата': salary,
        'Компания': company,
        'Город': city

    })

pprint(vacancy_list)


with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_list, f, ensure_ascii=False)






