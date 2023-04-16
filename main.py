import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

if response.ok:
    def get_links():
        section = soup.findAll('div', {'class': 'image_container'})
        for i in section:
            for p in i.find_all('a'):
                link = p['href']
                print(link)

    get_links()

    def get_next(pages_number):
        if soup.find('li', {'class': 'next'}):
            new_page = "page-"+pages_number+"html"
            url.replace("index.html", new_page)
            print(url)
        else:
            print("pas de next")

    """ nombre de page """
    pages = soup.find('li', {'class': 'current'}).text.strip()
    print(pages[len(pages)-1])









"""
if response.ok:
    with open('test.csv', 'w') as test:
        test.write('product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, '
                   'number_available, product_description, category, review_rating, image_url\n')

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text
        tds = soup.findAll('td')
        upc = tds[0].text
        priceAndTaxes = tds[2].text
        pricesNoTaxes = tds[3].text
        availability = tds[5].text
        description = soup.find('div', {'id': 'product_description'}).find_next('p').text
        category = soup.findAll('a')[3].text
        rating = soup.findAll('p')[2]['class'][1]
        img = soup.find('img')['src']

        test.write(url + '|' + upc + '|' + title + '|' + priceAndTaxes + '|' + pricesNoTaxes + '|' +
                   availability + '|' + description + '|' + category + '|' + rating + '|' + img + '\n')
                   """
