import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver

#'https://www.olx.ua/obyavlenie/shuba-iz-nutrii-IDJQpiM.html?sd=1#db858189d7;promoted
""""
.get_text(strip=True), Убирает пробелы
.get('href') выводит ссылки
"""""

def write_csv(comps):
    with open('cmc.csv', 'a' ) as file:
        order = [  'title', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=order)

        writer.writerow(comps)



def parser():
    url = 'https://www.olx.ua/transport/avtobusy/'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='space')
    urls = []


    for item in items:
        'получаем все ссылки'
        a = item.find('a', class_='thumb').get('href')
        links = {
                'href': f'https://www.olx.ua/{a}'
            }
        urls.append(links)

    for url in urls:
        r = requests.get(url['href'], headers=HEADERS)
        soup = BeautifulSoup(r.text, 'lxml')
        name = soup.find('a')

        print(name)



if __name__ == '__main__':
    parser()