
from utils import get_html

class Book:

    def __init__(self, book_url, category_name):
        self.product_page_url = []
        self.upc = []
        self.title = []
        self.price_including_tax = []
        self.price_excluding_tax = []
        self.number_available = []
        self.product_description = []
        self.category = category_name
        self.reviews_rating = []
        self.image_url = []
        self.html_soup = get_html(book_url)
        self.book_url = book_url

    def get_book(self):

        self.product_page_url= self.book_url
        tds = self.html_soup.find_all('td')
        self.upc = tds[0].text
        self.price_including_tax = tds[2].text
        self.price_excluding_tax = tds[3].text
        self.number_available = tds[5].text
        description = self.html_soup.find('div', {'id': 'product_description'})
        if description is None:
            self.product_description = ""
        else:
            self.product_description = description.find_next('p').text
        self.reviews_rating = self.html_soup.find_all('p')[2]['class'][1]
        self.image_url = (self.html_soup.find('img')['src']).replace('../..', 'http://books.toscrape.com')
        self.title = self.html_soup.find('h1').text
    