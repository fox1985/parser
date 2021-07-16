import requests
from bs4 import BeautifulSoup
import csv
import time
import re

"""
Простой парсер Яндекс Дзен Сделать простой парсер Яндекс.Дзен, на phph или программа не имеет значение. 
Сам парсер должен собирать только ссылки на каналы, к которым привязана соц сеть. Базу каналов он должен брать из https://zen.yandex.ru/media/zen/channels. 
Я указываю только номер страницы или канала с которого нужно начать. Ссылки должны сохраняться в текстовой документ, или таблицу эксель (на выбор разработчика).
"""

# 'https://zen.yandex.ru/media/zen/channels'
# https://zen.yandex.ru/media/zen/channels?page=1

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
}

def write_csv(data):
    with open('zen.csv', 'a') as f:
        witer = csv.writer(f)
        witer.writerow((data['title'],
                        data['link'],))

def parser():
    pattern = 'https://zen.yandex.ru/media/zen/channels?page={}'
    print("""
    Чтобы скачать 10 страниц надо набрать цифру 11.
    Или скачать 100 страниц надо набрать цифру 101.
    Если скачать  первую страницу надо набрать цифру 2
    """)
    print('='* 70 )

    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())

    for page in range(0, PAGENATION):
        url = pattern.format(str(page))
        print(f'Парсим страницу: {page}')





    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='channel-item__content')
    urls = []


    for item in items:
        a = item.find('a', class_='channel-item__link').get('href')

        links = {
            'href': f'https://zen.yandex.ru/{a}'
        }

        urls.append(links)


    for url in urls:
        try:
            r = requests.get(url['href'], headers=headers, )
            soup = BeautifulSoup(r.text, 'lxml')
            title = soup.find('span', class_='source-page-title-view__text').text
            soc = soup.find_all('li', class_='social-links-view__button')

        except:
            print('нет')


        for so in soc:
            link = so.find('a', class_='social-links-view__link')['href']

            #print(title)
            # print(link)
            # print('-' * 80)
            # print('=' * 80)

            data = {'title': title, 'link': link, }
            write_csv(data)


    #input("Всё конец Нажмите Enter чтобы выти ")





def main():
    parser()

if __name__ == '__main__':
    main()