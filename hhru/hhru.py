# -*- coding: utf-8 -*-
from datetime import time

import requests
from bs4 import BeautifulSoup
import shutil
import csv

headers = {'accept' : '*/*', 'user-agent' : 'Mozilla/baskino_parser.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36' }

base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&schedule=remote&text=python&page=0'



def hh_parser(base_url, headers):
    jobs = []
    urls = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')
        #переход по погинацыи
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url =f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&schedule=remote&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = BeautifulSoup(request.content, 'lxml')


        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                pras = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                content = text1 + '' + text2
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'content': content,
                    'pras': pras

                })
            except:
                pass

        print(len(jobs))


    else:
        print('ERROR or Done ' +  str(request.status_code))
    return jobs

def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание', 'цна'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content'], job['pras']) )

jobs = hh_parser(base_url, headers)
files_writer(jobs)