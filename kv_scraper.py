import re
from concurrent.futures import as_completed
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup, SoupStrainer
from requests_futures.sessions import FuturesSession
from geopy.extra.rate_limiter import RateLimiter
from src import init_app
from src.models import *

geolocator = Nominatim(user_agent="kv_scraper")
headers = {'User-Agent': 'Mozilla/5.0'}


def resolve_apartment_view(response, apartment, price):
    url = apartment.attrs['href'].replace("https://", "http://")
    strainer = SoupStrainer('div', attrs={'class': 'col-1-4 t-1-2'})
    apartment_soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer, from_encoding="utf8")
    broker_name = apartment_soup.find("div", {"class": "broker-name"})
    if broker_name:
        broker_name = broker_name.text.strip()
    broker_company = apartment_soup.find("a", {"class": "broker-company"})
    # No company in case the owner is selling
    if broker_company:
        broker_company = broker_company.text.strip()
    broker = Broker.query.filter(Broker.name == broker_name, Broker.company == broker_company).first()
    if not broker:
        broker = Broker(broker_name, broker_company)
        db.session.add(broker)
        db.session.commit()
    advert_id = int(''.join(re.findall(r'\d+', url.split('-')[-1])))
    address = apartment.text.strip()
    location = geolocator.geocode(address, timeout=None)

    latitude = location.latitude if location else None
    longitude = location.longitude if location else None

    table = apartment_soup.find("table", {"class": "table-lined object-data-meta"})
    if not table: return
    advert_rows = table.find("tbody").find_all("tr")

    apartment_stats = {}
    for row in advert_rows:
        th = row.find('th')
        td = row.find("td")
        if th and td:
            row_key = th.text.strip()
            row_value = td.text.strip()
            if row_key == 'Tube':
                apartment_stats['num_rooms'] = int(row_value)
            elif row_key == 'Üldpind':
                apartment_stats['square_meters'] = float(row_value.split('m')[0])
            elif row_key == 'Korrus/Korruseid':
                apartment_stats['floor'], apartment_stats['floors_in_building'] = [int(x) for x in
                                                                                   row_value.split('/')]
            elif row_key == 'Seisukord':
                apartment_stats['condition'] = row_value
            elif row_key == 'Omandivorm':
                apartment_stats['form_of_ownership'] = row_value
            elif row_key == 'Energiamärgis':
                apartment_stats['energy_efficiency'] = row_value
            elif row_key == 'Kulud suvel/talvel':
                # extract numbers from string
                row_value = re.findall(r'\d+', row_value)
                apartment_stats['utilities_summer'] = int(row_value[0]) if row_value else None
                apartment_stats['utilities_winter'] = int(row_value[1]) if 1 < len(row_value) else None
            elif row_key == 'Ehitusaasta':
                apartment_stats['build_year'] = int(row_value)

    if price and apartment_stats.get('square_meters'):
        square_meter_price = int(price / apartment_stats.get('square_meters'))

    Apartment.create(num_rooms=apartment_stats.get('num_rooms'),
                     square_meters=apartment_stats.get('square_meters'),
                     floor=apartment_stats.get('floor'),
                     floors_in_building=apartment_stats.get('floors_in_building'),
                     condition=apartment_stats.get('condition'),
                     form_of_ownership=apartment_stats.get('form_of_ownership'),
                     energy_efficiency=apartment_stats.get('energy_efficiency'),
                     utilities_summer=apartment_stats.get('utilities_summer'),
                     utilities_winter=apartment_stats.get('utilities_winter'),
                     build_year=apartment_stats.get('build_year'),
                     price=price,
                     square_meter_price=square_meter_price,
                     broker_id=broker.id,
                     address=address,
                     longitude=longitude,
                     latitude=latitude,
                     kv_id=advert_id
                     )


def resolve_menu_view(url, done=None, n=None):
    page = requests.get(url, headers=headers, stream=True)
    # parsing only partial page
    strainer = SoupStrainer('div', attrs={'main-content-wrap'})
    soup = BeautifulSoup(page.content, 'lxml', parse_only=strainer, from_encoding="utf8")
    # Find prices from menu
    prices = soup.find_all("p", {"class": "object-price-value"})
    apartments = soup.find_all("a", {"class": "object-title-a text-truncate"})
    apartment_urls = [a.attrs['href'].replace("https://", "http://") for a in apartments]

    if not done and not n:
        # get apartment count and initiate progressbar
        n = int(''.join(re.findall(r'\d+', soup.find("h1", {"class": "inner title"}).contents[0].text)))
        done = 0

    percentage = done / n * 100
    with FuturesSession(max_workers=6) as session:
        futures = [session.get(a, headers=headers) for a in apartment_urls]
        for i, future in enumerate(as_completed(futures)):
            # Most consistent place for price
            price = int(float(''.join(re.findall(r'\d+', prices[i].contents[0]))))
            resolve_apartment_view(future.result(), apartments[i], price)
            done += 1
            if percentage < int(done / n * 100):
                percentage = int(done / n * 100)
                print(percentage, '%')
    next_page_button = soup.find("li", {"class": "copy next"})
    if next_page_button:
        next_page = 'http://www.kv.ee/' + next_page_button.contents[0].attrs['href']
        resolve_menu_view(next_page, done, n)


def scrape_kv():
    start_url = "http://www.kv.ee/?act=search.simple&deal_type=1&search_type=old/"
    app = init_app()
    with app.app_context():
        # start with empty database
        Apartment.query.delete()
        Broker.query.delete()
        resolve_menu_view(start_url)
    print('All Done')


if __name__ == "__main__":
    scrape_kv()
