# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import shutil


count = 1
while count <= 1:  # страница сайта для пирибора по навигацыи

    headers = {'accept' : '*/*', 'user-agent' : 'Mozilla/baskino_parser.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36' }

    base_url = 'http://baskino.me/page/' + str(count)



    def baskino_parser(base_url, headers):
        session = requests.Session()
        request = session.get(base_url, headers=headers)

        if request.status_code == 200:
            soup = BeautifulSoup(request.content,  'html.parser')
            divs = soup.find_all('div', {'class': 'shortpost'})
            for div in divs:
                post_title = div.find('div', {'class': 'posttitle'})
                link = post_title.find('a').text
                print(link)

                # классы картинки
                img = div.find('div', {'class': 'postcover'})
                img_src = img.find('img').get('src')
                src = img_src

                # скачивает картинки
                response = requests.get(src, stream=True)
                with open(link.replace('/', '') + '.jpg', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response

        else:
            print('ERROR')

    count += 1

    baskino_parser(base_url, headers)
