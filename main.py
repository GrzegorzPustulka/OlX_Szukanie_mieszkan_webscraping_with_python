import functions

name_advertisements = []
link_advertisements = []
prices = []
locations = []
descriptions = []
areas = []
rents = []
real_prices = []
current_page = 1

# wybór miasta
base_url = functions.page()

max_price = int(input('Podaj maksymalna cene mieszkania: '))
min_price = int(input('Podaj minimalna cene mieszkania: '))
page = int(input('Ile podstron chcesz przejrzeć: '))
print(base_url)

# wyszukuje link, cene i lokalizacje oferty
functions.scraping(current_page, page, base_url, name_advertisements, link_advertisements, locations, prices)

# Wyszkujuje opisy ofert i powierzchnie
functions.find_description(link_advertisements, descriptions, areas, rents)

# zamienia "brzydkie" dane liczbowe i ciagi tekstu na liczby
number_price = functions.change_price_to_number(prices, rents, real_prices)

# wybiera dane interesujace mnie do przegladania
my_value = functions.final_data(number_price, max_price, link_advertisements, name_advertisements, locations, descriptions, areas, rents,real_prices,min_price)

print(my_value)
with open('dane.txt', 'w', encoding='utf-8') as f:
    f.write(my_value)
