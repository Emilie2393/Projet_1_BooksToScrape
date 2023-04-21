import requests
from bs4 import BeautifulSoup


home_url = "http://books.toscrape.com/index.html"

response = requests.get(home_url)
soup = BeautifulSoup(response.text, 'html.parser')

category_url = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
for i in category_url:
    link = i['href']
    print(link)

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
                link_href = p['href']
                link = link_href.replace("../../..", "http://books.toscrape.com/catalogue")
                links.append(link)

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

    """get book's links"""
    if pages_check is not None:
        pages_strip = pages_check.text.strip()
        pages_number = pages_strip[len(pages_strip) - 1]
        for page in range(1, (int(pages_number) + 1)):
            """ get index.html links only """
            if page == 1:
                get_links(url)
            else:
                """get next url page and get their product's links"""
                get_next(str(page), url)
                get_links(url)
    else:
        get_links(url)

    """with open('test.csv', 'w', encoding="utf-8") as test:
        test.write('product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,'
                   'product_description, category, review_rating, image_url\n')

        for j in links:
            url = j
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.ok:
                tds = soup.findAll('td')
                upc = tds[0].text
                priceAndTaxes = tds[2].text
                pricesNoTaxes = tds[3].text
                availability = tds[5].text
                description = soup.find('div', {'id': 'product_description'}).find_next('p').text
                description_bug = description.replace(';', ',')
                category = soup.findAll('a')[3].text
                rating = soup.findAll('p')[2]['class'][1]
                img = soup.find('img')['src']
                title = soup.find('h1').text
                test.write(url + '|' + upc + '|' + title + '|' + priceAndTaxes + '|' + pricesNoTaxes + '|' +
                           availability + '|' + description_bug + '|' + category + '|' + rating + '|' + img + '\n')"""

