import requests
from bs4 import BeautifulSoup
import pandas as pd

home_url = "http://books.toscrape.com/index.html"

response = requests.get(home_url)
soup = BeautifulSoup(response.text, 'html.parser')

category_list = []
category_urls = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')
for i in category_urls:
    category_url = i['href']
    """ correct category's url """
    new_home_url = home_url.replace("/index.html", "")
    full_link = (new_home_url + '/' + category_url)
    category_list.append(full_link)
""" delete home page from category_list """
category_list.pop(0)

for f in category_list:

    url = f
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

        """get category name for csv name"""
        category_name = soup.find('h1').text

        """with open((category_name + '.csv'), 'w', encoding="utf-8") as data:
            data.write('product_page_url' + ',' + 'upc' + ',' + 'title' + ',' + 'price_including_tax' + ','
                       + 'price_excluding_tax' + ',' + 'number_available' + ',' + 'product_description' + ',' +
                       'category' + ',' + 'review_rating' + ',' + 'image_url' + '\n')"""

        products_page_url = []
        upc = []
        title = []
        price_including_tax = []
        price_excluding_tax = []
        number_available = []
        product_description = []
        category = []
        review_rating = []
        image_url = []

        for j in links:
            url = j
            products_page_url.append(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.ok:
                tds = soup.findAll('td')
                upc.append(tds[0].text)
                price_including_tax.append(tds[2].text[2:7])
                price_excluding_tax.append(tds[3].text[2:7])
                number_available.append(tds[5].text)
                description = soup.find('div', {'id': 'product_description'})
                if description is None:
                    product_description.append("")
                else:
                    product_description.append(description.find_next('p').text)
                    """product_description.append(description.replace(',', ' '))"""
                category.append(category_name)
                review_rating.append(soup.findAll('p')[2]['class'][1])
                image_url.append(soup.find('img')['src'])
                title.append(soup.find('h1').text)

        datas = {
            'products_page_url': products_page_url,
            'upc': upc,
            'title': title,
            'price_excluding_tax': price_excluding_tax,
            'price_including_tax': price_including_tax,
            'number_available': number_available,
            'product_description': product_description,
            'category': category,
            'review_rating': review_rating,
            'image_url': image_url
        }

        df = pd.DataFrame(datas)
    df.to_csv((category_name + '.csv'), index=False, sep=',', encoding='utf-8')
    df

    print(title)
    print(product_description)
