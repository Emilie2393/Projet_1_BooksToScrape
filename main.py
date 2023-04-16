import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = []

if response.ok:
    def get_links(next_url):
        next_response = requests.get(next_url)
        next_soup = BeautifulSoup(next_response.text, 'html.parser')
        section = next_soup.findAll('div', {'class': 'image_container'})
        for i in section:
            for p in i.find_all('a'):
                link = p['href']
                links.append(link)
        return links

    def get_next(pages, next_url):
        new_page = "page-" + pages + ".html"
        if "index.html" in next_url:
            new_url = next_url.replace("index.html", new_page)
        else:
            old_page = int(pages) - 1
            text_page = str(old_page)
            new_url = next_url.replace(("page-" + text_page + ".html"), new_page)
        global url
        url = new_url
        return url


    """pages number or None"""
    pages_check = soup.find('li', {'class': 'current'})
    pages_strip = pages_check.text.strip()
    pages_number = pages_strip[len(pages_strip) - 1]

    """get book's links"""
    if pages_check is not None:
        for page in range(1, (int(pages_number) + 1)):
            """ get index.html links only """
            if page == 1:
                get_links(url)
                print(get_links(url))
            else:
                """get next url page and get their product's links"""
                get_next(str(page), url)
                get_links(url)
        print(links)

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
