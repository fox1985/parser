
import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

html = get_html(URL)


def get_content(html):
    soup =BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-item')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='title').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='title').find('a').get('href'),
                'brand': item.find('div', class_='brand').get_text(strip=True),
                'card_img': HOST + item.find('div', class_='image').find('img').get('src'),
            }
        )
    return cards




def save_doc(items, path, ):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Ссылка на продукт', 'Банк', 'Изображение карты',])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['brand'], item['card_img']])

def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}' )
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)

    else:
        print('Error')

parser()

