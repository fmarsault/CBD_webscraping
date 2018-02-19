import urllib2
from bs4 import BeautifulSoup
# import builtwith


def spider(url):
    """ Scrapper return the html page parsed by BeautifulSoup """
    page = urllib2.urlopen(auchan_page)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def info_product(soup):
    """ Return the name, price and seller of the product page."""
    name_box = str(soup.find('h1')).split('<br/>')
    name = name_box[0].replace("<h1>","")
    seller = name_box[1].replace("</h1>","")
    price_box = soup.find('span', attrs={'itemprop': 'price'}).text
    price = float(price_box.replace('u','').replace(",","."))
    product_entry = [name, seller, price]

    return product_entry

auchan_page = 'https://www.auchan-supermarche.fr/acheter-activia-nature-danone-12x125g-danone,143577,111,881,3841.htm'

soup =spider(auchan_page)
product_entry = info_product(soup)
print(product_entry)





