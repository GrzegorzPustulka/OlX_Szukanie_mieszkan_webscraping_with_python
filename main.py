import functions
import pandas as pd

name_advertisements = []
link_advertisements = []
prices = []
locations = []
areas = []
rents = []
real_prices = []
current_page = 1

base_url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?page={}'
page = int(input('Ile podstron chcesz przejrzeć: '))


# wyszukuje link, cene i lokalizacje oferty
functions.scraping(current_page, page, base_url, name_advertisements, link_advertisements, locations, prices)

# Wyszkujuje opisy ofert i powierzchnie
functions.find_description(link_advertisements, areas, rents)

# zamienia "brzydkie" dane liczbowe i ciagi tekstu na liczby
number_price = functions.change_price_to_number(prices, rents, real_prices)

df = pd.DataFrame({
    'nazwa ogłoszenia': name_advertisements,
    'lokalizacja': locations,
    'powierzchnia': areas,
    'cena': number_price,
    'czynsz': rents,
    'cena całkowita': real_prices,
    'link do ogłoszenia': link_advertisements})


df.to_excel('OlxDane.xlsx', sheet_name='Dane')
