from utils import get_html, get_links, get_next

class Categories:

    def __init__(self):

        self.categories_url_list = []
        self.category_books = []
        self.home_url = "http://books.toscrape.com/index.html"
        self.soup = get_html(self.home_url)
        self.name = ""
        


    """get one category link to add to self.category_list"""


    def get_category(self, cat_url):

        home_url = self.home_url
        category_url = cat_url['href']
        """ correct category's url """
        new_home_url = home_url.replace("/index.html", "")
        full_link = (new_home_url + '/' + category_url)
        self.categories_url_list.append(full_link)
        self.name = get_html(full_link).find('h1').text

    
    """scrap the main page to add each category to self.category_list"""
    

    def get_category_list(self):

        category_urls = self.soup.find('ul', {'class': 'nav nav-list'}).find_all('a')

        for i in category_urls:
            # complete the category_list variable bellow
            self.get_category(i)

        """ delete home page from category_list """
        self.categories_url_list.pop(0)


    """add each book link to self.category_books"""


    def get_books_list(self, url):
        
        """pages number or None"""
        book_soup = get_html(url)
        pages_check = book_soup.find('li', {'class': 'current'})
        self.name = book_soup.find('h1').text
        """get book's links of each pages"""
        if pages_check is not None:
            pages_strip = pages_check.text.strip()
            pages_number = pages_strip[len(pages_strip) - 1]
            for page in range(1, (int(pages_number) + 1)):
                """ get index.html links only """
                if page == 1:
                    self.category_books.extend(get_links(url))
                else:
                    """get next url page and get their product's links"""
                    self.category_books.extend(get_links(get_next(str(page), url)))
        else:
            self.category_books.extend(get_links(url))
