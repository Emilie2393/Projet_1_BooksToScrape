import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import threading

"""get html source"""


def get_html(from_url):
    try:
        r = requests.get(from_url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    except requests.exceptions.HTTPError as err:
        print("HTTP Error", err)


"""complete books_list with books of one page"""


def get_links(next_url):
    books_list = []
    next_soup = get_html(next_url)
    section = next_soup.findAll('div', {'class': 'image_container'})
    for books in section:
        """ get all links in each div """
        for a in books.find_all('a'):
            link_href = a['href']
            link = link_href.replace("../../..", "http://books.toscrape.com/catalogue")
            books_list.append(link)
    return books_list


"""get next page of a category"""


def get_next(pages, next_url):
    new_page = "page-" + pages + ".html"
    if "index.html" in next_url:
        new_url = next_url.replace("index.html", new_page)
    else:
        old_page = int(pages) - 1
        text_page = str(old_page)
        new_url = next_url.replace(("page-" + text_page + ".html"), new_page)
    url = new_url
    return url


"""complete category list with each category's url"""


def get_category(cat_url):
    category_url = cat_url['href']
    """ correct category's url """
    new_home_url = home_url.replace("/index.html", "")
    full_link = (new_home_url + '/' + category_url)
    category_list.append(full_link)


home_url = "http://books.toscrape.com/index.html"

soup = get_html(home_url)

category_list = []
category_urls = soup.find('ul', {'class': 'nav nav-list'}).findAll('a')

for i in category_urls:
    get_category(i)

""" delete home page from category_list """
category_list.pop(0)

first_half_list = int((len(category_list)) / 2)


def final_scraping(book):
    url = book
    soup = get_html(url)

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

    links1 = []
    links2 = []
    links3 = []

    """pages number or None"""
    pages_check = soup.find('li', {'class': 'current'})

    """get book's links of each pages"""
    if pages_check is not None:
        pages_strip = pages_check.text.strip()
        pages_number = pages_strip[len(pages_strip) - 1]
        for page in range(1, (int(pages_number) + 1)):
            """ get index.html links only """
            if page == 1:
                links1 = get_links(url)
            else:
                """get next url page and get their product's links"""
                links2 = get_links(get_next(str(page), url))
    else:
        links3 = get_links(url)

    books_list = links1 + links2 + links3

    """get category name for csv file"""
    category_name = soup.find('h1').text

    for j in books_list:
        book_url = j
        book_soup = get_html(book_url)

        """get one book"""

        def get_book(html_soup):
            products_page_url.append(book_url)
            tds = html_soup.findAll('td')
            upc.append(tds[0].text)
            prices_including_tax.append(tds[2].text)
            prices_excluding_tax.append(tds[3].text)
            number_available.append(tds[5].text)
            description = html_soup.find('div', {'id': 'product_description'})
            if description is None:
                products_description.append("")
            else:
                products_description.append(description.find_next('p').text)
            category.append(category_name)
            reviews_rating.append(html_soup.findAll('p')[2]['class'][1])
            images_url.append((html_soup.find('img')['src']).replace('../..', 'http://books.toscrape.com'))
            titles.append(html_soup.find('h1').text)

        get_book(book_soup)

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
        img_title = (re.sub("[':,;!#*?/.-]", '', titles[title])).replace(" ", "_").replace('"', '')
        titles[title] = img_title
    """path attribution for each images with urllib.request"""
    for img in range(len(images_url)):
        path = category_name + "/" + titles[img] + ".jpg"
        urllib.request.urlretrieve(images_url[img], path)


def first_half():
    for i in range(first_half_list):
        final_scraping(category_list[i])


def second_half():
    for e in range((first_half_list + 1), len(category_list)):
        final_scraping(category_list[e])


thread1 = threading.Thread(target=first_half)
thread2 = threading.Thread(target=second_half)
thread1.start()
thread2.start()
