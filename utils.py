import requests
from bs4 import BeautifulSoup

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
    section = next_soup.find_all('div', {'class': 'image_container'})
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
