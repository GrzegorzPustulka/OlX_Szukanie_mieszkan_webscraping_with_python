import re
import bs4
import requests
import sys


def page():
    print("wybierz 1 jeśli chcesz przeglądać mieszkania z krakowa\nwybierz 2 jeśli sam chcesz wybrać miasto")
    choose = input("Mój wybór to: ")
    if choose == '1':
        link = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?page={}'
    elif choose == '2':
        link = input("wklej tutaj link: ")
        link = link + '?page={}'
    else:
        print('nie bylo takiego wyboru')
        sys.exit(2)
    return link


def scraping(current_page, page, base_url, name_advertisements, link_advertisements, locations, prices):
    s = 0
    try:
        while current_page <= page:
            req = requests.get(base_url.format(current_page))
            soup = bs4.BeautifulSoup(req.text, 'lxml')
            for name in soup.select('.lheight22.margintop5'):
                name_advertisements.append(name.text)

            for price in soup.select('.price'):
                prices.append(price.text)

            prices.pop(s)  # usuwa pierwszy element bo to nie cena
            prices.pop(s)  # usuwa drugi element bo to nie cena
            if len(prices) % 44 == 0:
                s += 44
            else:
                s += len(prices) % 44

            if (len(name_advertisements) % 44) == 0:
                for i in range(0, 44):
                    link_advertisements.append(soup.select('.marginright5')[i]['href'])

                j = 1
                while j < 132:
                    locations.append(soup.select('.breadcrumb.x-normal')[j].getText())
                    j += 3
            else:
                j = len(name_advertisements) % 44
                s = 0
                while s < j:
                    link_advertisements.append(soup.select('.marginright5')[s]['href'])
                    s += 1

                s = 1
                while s < 3 * j:
                    locations.append(soup.select('.breadcrumb.x-normal')[s].getText())
                    s += 3

            current_page += 1

    except IndexError:
        print('nie ma tyle stron do przejrzenia')
        sys.exit(1)


def find_description(link_advertisements, descriptions, areas, rents):
    for link in link_advertisements:
        text = ''

        req = requests.get(link)
        soup = bs4.BeautifulSoup(req.text, 'lxml')

        if 'olx.pl' in link:
            try:
                descriptions.append(soup.select_one('.css-g5mtbi-Text').getText())
            except AttributeError:
                descriptions.append('Niespodziewany brak opisu/powierzchni')
            for tag in soup.select('.css-xl6fe0-Text.eu5v0x0'):
                text += tag.getText()
                if 'Powierzchnia' in tag.getText():
                    areas.append(tag.getText())
                if 'Czynsz' in tag.getText():
                    rents.append(tag.getText())
            if 'Czynsz' not in text:
                rents.append('0 zł')

        else:
            descriptions.append('Musisz wejsc na strone OtoDom')  # Do zrobienia
            for tag in soup.select('.css-1wi2w6s.estckra5'):
                text += tag.getText()
                if 'miesiąc' in tag.getText():
                    rents.append(tag.getText())
                if 'm²' in tag.getText():
                    areas.append(tag.getText())
            if 'miesiąc' not in text:
                rents.append('0 zł')
            if 'm²' not in text:
                areas.append('Brak podanej powierzchni')


def change_price_to_number(prices, rents, real_prices):
    text_prices = ''
    text_rents = ''
    for price in prices:
        text_prices += price
    for rent in rents:
        text_rents += rent
    text_prices = text_prices.replace(' ', '')
    text_prices = text_prices.replace(',', '.')
    text_rents = text_rents.replace(' ', '')
    text_rents = text_rents.replace('zł', ' ')
    text_rents = text_rents.replace(',', '.')
    number_price = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_prices)]
    number_rent = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_rents)]

    for i in range(0, len(prices)):
        real_prices.append(number_price[i] + number_rent[i])
    return number_price


def final_data(number_price, max_price, link_advertisements, name_advertisements, locations, descriptions, areas, rents, real_prices, min_price):

    my_value = ''
    counter = 1

    for i in range(0, len(number_price)):
        if (max_price >= real_prices[i]) and (min_price <= real_prices[i]):
            my_value = 'Ogłoszenie numer ' + str(counter) + '|' + link_advertisements[i] + '|' + name_advertisements[i] + '|' + locations[i] + '|' + str(number_price[i]) + 'zł|' + str(rents[i]) + '|' + 'cena całkowita: ' + str(real_prices[i]) + 'zł|' + areas[i] + '|' + descriptions[i] + '|||' + my_value
            counter += 1
        else:
            continue
    my_value = my_value.replace('\n', '')
    my_value = my_value.replace('|', '\n')
    return my_value
