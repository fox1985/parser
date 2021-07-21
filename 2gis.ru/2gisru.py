import requests
from  selenium import  webdriver
from bs4 import BeautifulSoup
import csv
# https://2gis.ru/moscow/search/%D0%9A%D1%80%D0%B0%D1%81%D0%BE%D1%82%D0%B0

#https://2gis.ru/moscow/search/%D0%9A%D1%80%D0%B0%D1%81%D0%BE%D1%82%D0%B0/page/{}

#https://2gis.ru/moscow/search/%D0%9A%D1%80%D0%B0%D1%81%D0%BE%D1%82%D0%B0/page/3?m=38.158434%2C55.741031%2F9.7




def gis_csv(data):
    with open('gis.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'], data['email'], ])


def parser():
    """парсит прохотдит на вторую страницу обевления """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }
    #перебор по пагинации
    i = 0
    while i <= 5:
        url = f"https://2gis.ru/moscow/search/%D0%9A%D1%80%D0%B0%D1%81%D0%BE%D1%82%D0%B0/page/{i}"
        i += 1


    base_url = "https://2gis.ru/moscow/search/"

    response = requests.get(url,  headers=headers)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")


    products = soup.find_all("div", {"class": "_1h3cgic"})

    urls = []
    for cont in products:
        """Переходит посылки товара и получамем все ссылки салоны"""
        url = cont.select_one("a")["href"]
        urls.append(base_url + "/" + url.replace("../", ""))


    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            name = soup.find("h1").text
            tele = soup.find('div', {"class": "_b0ke8"}).find_next('a')['href'].replace("tel:", "")
            email = soup.find('div', {"class": "_49kxlr"}).find_next('a', {"class": "_1nped2zk"}).find_next('div').find_next('a', {"class": "_1nped2zk"}).find_next('a', {"class": "_1nped2zk"}).text.replace("2GIS, OpenStreetMap contributors", "")

            #data = {'name': name, 'email': email}

            #gis_csv(data)

            print(name, '-' , tele, email)





        except:
            print("нет")





parser()

