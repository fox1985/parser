import requests
from bs4 import BeautifulSoup as bs
import csv


class Bot:
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
               'User-Agent:' 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
               }

    def __int__(self):
        self.get_html()

    def get_html(self):
        url = "https://www.avito.ru/rossiya/nedvizhimost"
        with requests.Session() as session:
            response = session.get(url, headers=self.headers)
        return response.text

    def parser_html(self, html):
        urls = []
        soup = bs(html, 'lxml')
        main_div = soup.find_all('div', {'class': 'body-titleRow-1UZUF'})
        # получаем все ссылки
        for data in main_div:
            a = data.find('a', {'class': 'link-link-39EVK'})['href']
            links = {
                'href': f'https://www.avito.ru{a}'
            }
            urls.append(links)

        # Выводит имя продовца
        for user in urls:
            r = requests.get(user['href'], headers=self.headers)
            soup = bs(r.text, 'lxml')
            name = soup.find('div', {'class': 'seller-info-name'}).text
            id_nomer = soup.find('div', {'class': 'item-view-search-info-redesign'}).text
            phone = soup.find('div', {'class': 'title-info-metadata-views'}).text
            print(id_nomer)











def main():
    """Вызываем класс бот"""
    bot = Bot()
    html = bot.get_html()
    rezult = bot.parser_html(html)
    print(rezult)

if __name__ == '__main__':
    main()