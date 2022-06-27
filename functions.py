import re
import bs4
import numpy as np
import requests
import sys


def scraping(current_page, page, base_url, name_advertisements, link_advertisements, locations, prices):
    try:
        x = 0
        while current_page <= page:

            req = requests.get(base_url.format(current_page))
            soup = bs4.BeautifulSoup(req.text, 'lxml')

            for name in soup.select('.css-v3vynn-Text.eu5v0x0'):
                name_advertisements.append(name.text)
                x += 1

            for price in soup.select('p.css-wpfvmn-Text.eu5v0x0'):
                prices.append(price.text)

            for i in range(0, x):
                if 'www.otodom.pl' in soup.select('a.css-1bbgabe')[i]['href']:
                    link_advertisements.append(soup.select('a.css-1bbgabe')[i]['href'])
                else:
                    link_advertisements.append('http://olx.pl' + soup.select('a.css-1bbgabe')[i]['href'])
                locations.append(soup.select('p.css-p6wsjo-Text.eu5v0x0')[i].getText())

            x = 0
            current_page += 1

    except IndexError:
        print('nie ma tyle stron do przejrzenia')
        sys.exit(1)


def find_description(link_advertisements, areas, rents):
    for link in link_advertisements:
        text = ''
        req = requests.get(link)
        soup = bs4.BeautifulSoup(req.text, 'lxml')

        if 'olx.pl' in link:
            for tag in soup.select('.css-xl6fe0-Text.eu5v0x0'):
                text += tag.getText()
                if 'Powierzchnia' in tag.getText():
                    areas.append(tag.getText())
                if 'Czynsz' in tag.getText():
                    rents.append(tag.getText())
            if 'Czynsz' not in text:
                rents.append('0 zł')
            if 'Powierzchnia' not in text:
                areas.append(np.nan)
        else:
            for tag in soup.select('.css-1wi2w6s.estckra5'):
                text += tag.getText()
                if 'miesiąc' in tag.getText():
                    rents.append(tag.getText())
                if 'm²' in tag.getText():
                    areas.append(tag.getText())
            if 'miesiąc' not in text:
                rents.append('0 zł')
            if 'm²' not in text:
                areas.append(np.nan)


def change_price_to_number(prices, rents, real_prices):
    text_prices = ''
    text_rents = ''
    for price in prices:
        text_prices += price
    for rent in rents:
        text_rents += rent
    text_prices = text_prices.replace(' ', '').replace(',', '.')
    text_rents = text_rents.replace(' ', '').replace('zł', ' ').replace(',', '.')
    number_price = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_prices)]
    number_rent = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_rents)]

    for i in range(0, len(prices)):
        real_prices.append(number_price[i] + number_rent[i])
    return number_price


