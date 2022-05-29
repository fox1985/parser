import requests
from bs4 import BeautifulSoup
import json

PAGES_COUNT = 1
OUT_FILENAME = 'qut.json'

def get_soup(url, **kwargs):
    reponse = requests.get(url, **kwargs)
    if reponse.status_code == 200:
        soup = BeautifulSoup(reponse.text, features='html.parser')
    else:
        soup = None

    return soup


def crewl_products(pages_counl):
    urls = []
    fmt = 'https://parsemachine.com/sandbox/catalog/?page={page}'

    for page_n in range(1, 1 + pages_counl):
        print('page: {}'.format(page_n))

        page_url = fmt.format(page=page_n)
        soup = get_soup(page_url)
        if soup is None:
            break

        for tag in soup.select('.product-card .title'):
            href = tag.attrs['href']
            url = 'https://parsemachine.com{}'.format(href)
            urls.append(url)
    return urls


def parse_prodoucts(urls):
    data = []
    for url in urls:
        soup = get_soup(url)
        if soup is None:
            break
        name = soup.select_one('#product_name').text.strip()
        amount = soup.select_one('#product_amount').text.strip()
        description = soup.select_one('#description').text.strip()
        techs = {}

        for row in soup.select('#characteristics tbody tr'):
            cols = row.select('td')
            cols = [c.text.strip() for c in cols]
            techs[cols[0]] = cols[1]

            item = {
                'name': name,
                'amount': amount,
                'techs': techs,
                'description': description,
            }

            data.append(item)
    return data


def main():
    urls = crewl_products(PAGES_COUNT)
    print('\n'.join(urls))
    data =parse_prodoucts(urls)

    with open(OUT_FILENAME, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()