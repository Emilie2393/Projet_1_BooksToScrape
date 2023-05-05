import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

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
            for books in section:
                """ get all links in each div """
                for a in books.find_all('a'):
                    link_href = a['href']
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

        """get category name for csv file"""
        category_name = soup.find('h1').text

        products_page_url = []
        upc = []
        titles = []
        prices_including_tax = []
        prices_excluding_tax = []
        number_available = []
        products_description = []
        category = []
        reviews_rating = []
        images_url = []

        for j in links:
            url = j
            products_page_url.append(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if response.ok:
                tds = soup.findAll('td')
                upc.append(tds[0].text)
                prices_including_tax.append(tds[2].text)
                prices_excluding_tax.append(tds[3].text)
                number_available.append(tds[5].text)
                description = soup.find('div', {'id': 'product_description'})
                if description is None:
                    products_description.append("")
                else:
                    products_description.append(description.find_next('p').text)
                category.append(category_name)
                reviews_rating.append(soup.findAll('p')[2]['class'][1])
                images_url.append((soup.find('img')['src']).replace('../..', 'http://books.toscrape.com'))
                titles.append(soup.find('h1').text)

        datas = {
            'products_page_url': products_page_url,
            'upc': upc,
            'titles': titles,
            'prices_excluding_tax': prices_excluding_tax,
            'prices_including_tax': prices_including_tax,
            'number_available': number_available,
            'products_description': products_description,
            'category': category,
            'reviews_rating': reviews_rating,
            'images_url': images_url
        }

        """pandas dataframe and proper encoding"""
        dataframe = pd.DataFrame(datas)
        dataframe.to_csv((category_name + '.csv'), index=False, sep=',', encoding='utf-8-sig')

        """images file creation with os"""
        os.mkdir(category_name)

        """titles modification"""
        for title in range(len(titles)):
            img_title = (re.sub("[':,;!#*!?/.-]", '', titles[title])).replace(" ", "_").replace('"', '')
            titles[title] = img_title

        """path attribution for each images with urllib.request"""
        for img in range(len(images_url)):
            path = "c:/Users/Emilie/Desktop/Formation_INFO/OPENCLASSROOMS/PYTHON/PROJET 2/BOOKSTOSCRAP_RICHARD_EMILIE/" + \
                   category_name + "/" + titles[img] + ".jpg"
            urllib.request.urlretrieve(images_url[img], path)

        print(titles)

