import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    tds = soup.findAll('td')
    upc = tds[0]
    priceAndTaxes = tds[2]
    pricesNoTaxes = tds[3]
    availability = tds[5]

    print(title.text, upc.text, priceAndTaxes.text, pricesNoTaxes.text)

"""
with open('urls.csv', 'w') as file:
    file.write(str(title))*
"""

