from bs4 import BeautifulSoup
import requests
import csv

def write_csv(data):
    with open('number.csv', 'a') as f:
        witer = csv.writer(f)
        witer.writerow((data['number'],))


def parser_page():
    pattern = 'https://www.nomerogram.ru/page{}.html'
    print("""Чтобы скачать 5 страниц надо набрать цифру 6 .""")

    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())

    for i in range(2, PAGENATION):
        url = pattern.format(str(i))

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    items = soup.find_all('div', class_='ng-number')
    urls = []

    for item in items:
        number = item.find('div', class_='ng-number__number').text
        print(number)

        data = {'number': number, }
        write_csv(data)





def main():
    parser_page()



if __name__ == '__main__':
    main()
