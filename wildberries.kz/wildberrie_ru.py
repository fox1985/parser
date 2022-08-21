
import  requests
from bs4 import BeautifulSoup
import csv
import re
FILE = 'top.csv'

""""
Функционал: 
1. Сбор информации по конкретному разделу товаров(название, ссылка, цена, изменение цены).
2. Экспорт полученной информации в Excel таблицу. 

"""""
""""
.get_text(strip=True), Убирает пробелы
.get('href') выводит ссылки
"""""



def get_html(url):

    pages = requests.get(url)
    pages.encoding = 'utf8'
    if pages.ok:
        return pages.text
    print(pages.status_code)




def save_file(items, path):
    with open(path, 'w',) as file:
        writer = csv.writer(file,)
        writer.writerow(['Марка', 'что это', 'Цена', 'Скидка', 'Ссылка', ])
        for item in items:
            writer.writerow([item['brand_name'], item['name'], item['price'],item['link'], ], )




def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result




def get_page_data(html):
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    container = soup.select('div.catalog-page__content')


    for con in container:

        brand_name = con.find('strong', class_='brand-name').text
        goods_name = con.find('span', class_='goods-name').text
        price = con.find('span', class_='price').text
        a = con.find('a', class_='j-open-full-product-card')['href']
        links = {
            'href': f'https://www.wildberries.ru{a}'
        }
        urls.append(links)

        print(brand_name, goods_name, price, links)




    # Читает даные со второй страницы
    for page in urls:
        r = requests.get(page['href'],)
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('h1', class_='title').text
        composition = soup.find('span', class_='j-composition').text
        print(title, composition)










def main():
    url = 'https://www.wildberries.ru/brands/xiaomi/all'
    get_page_data(get_html(url))



if __name__ == '__main__':
    main()