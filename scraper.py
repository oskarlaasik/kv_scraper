import requests as requests
from bs4 import BeautifulSoup

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

URL = "http://www.kv.ee/?act=search.simple&deal_type=1&search_type=old/"
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
headers={'User-Agent': 'Mozilla/5.0'}
page = requests.get(URL, headers=headers, timeout=15)
soup = BeautifulSoup(page.content, 'html.parser')
appartments = soup.find_all("a", {"class": "object-title-a text-truncate"})
next_page = soup.find("li", {"class": "next"})
data = {}
for appartment in appartments:
    appartment_url = appartment.attrs['href'].replace("https://","http://")
    appartment_page = requests.get(appartment_url, headers=headers, timeout=15)
    appartment_soup = BeautifulSoup(appartment_page.content, 'html.parser')
    advert_unique_id = appartment_soup.find("span", {"class": "copy-object-link"}).next

    advert_rows = appartment_soup.find("table", {"class": "table-lined object-data-meta"})\
        .find("tbody").find_all("tr")


    for row in advert_rows:
        th = row.find('th')
        td = row.find("td")
        if th and td:
            row_key = th.text.strip()
            row_value = td.text.strip()
            data[row_key] = row_value
print()

