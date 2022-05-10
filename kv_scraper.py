import requests
from bs4 import BeautifulSoup
import re
from src import init_app
from src.models import *


headers={'User-Agent': 'Mozilla/5.0'}

#dict_keys(['Tube', 'Üldpind', 'Korrus/Korruseid', 'Ehitusaasta', 'Seisukord', 'Omandivorm', 'Katastrinumber', 'Energiamärgis', 'Kulud suvel/talvel', 'Kinnistu number', 'Korruseid'])

def resolve_appartment_view(appartment):
        appartment_url = appartment.attrs['href'].replace("https://", "http://")
        appartment_page = requests.get(appartment_url, headers=headers)
        appartment_soup = BeautifulSoup(appartment_page.content, 'html.parser')
        advert_unique_id = appartment_soup.find("span", {"class": "copy-object-link"}).next
        price = float(''.join(re.findall(r'\d+', appartment_soup.find("div", {"class": "object-price"})
                                         .find('strong').string)))
        advert_rows = appartment_soup.find("table", {"class": "table-lined object-data-meta"}) \
            .find("tbody").find_all("tr")
        for row in advert_rows:
            th = row.find('th')
            td = row.find("td")
            if th and td:
                row_key = th.text.strip()
                row_value = td.text.strip()
                print()
                if row_key == 'Tube':
                    rooms = int(row_value)
                elif row_key == 'Üldpind':
                    square_meters = row_value
                elif row_key == 'Korrus/Korruseid':
                    floor, floors_in_building = [int(x) for x in row_value.split('/')]
                elif row_key == 'Seisukord':
                    condition = row_value
                elif row_key == 'Omandivorm':
                    form_of_ownership = row_value
                elif row_key == 'Energiamärgis':
                    energy_efficiency = row_value
                elif row_key == 'Kulud suvel/talvel':
                    utilities_summer, utilities_winter = [int(x) for x in re.findall(r'\d+', row_value)]
                elif row_key == 'Tube':
                    num_rooms = int(row_value)
                elif row_key == 'Ehitusaasta':
                    build_year = int(row_value)


def resolve_menu_view(URL):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    appartments = soup.find_all("a", {"class": "object-title-a text-truncate"})
    next_page = soup.find("li", {"class": "next"})
    for appartment in appartments:
        resolve_appartment_view(appartment)

def scrape_kv():
    start_url = "http://www.kv.ee/?act=search.simple&deal_type=1&search_type=old/"
    app = init_app()
    with app.app_context():
        #start with empty database
        Appartment.query.delete()
        resolve_menu_view(start_url)
        db.session.commit()

if __name__ == "__main__":
    scrape_kv()