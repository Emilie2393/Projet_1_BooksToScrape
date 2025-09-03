from categories import Categories
from book import Book
from category import Category

class BookScraper:
    def __init__(self):
        self.categories = Categories()
    
    def scrape_all_categories(self):
        """Fetch all categories and scrape books for each one."""
        self.categories.get_category_list()
        for category_url in self.categories.categories_url_list:
            self.scrape_category(category_url)
    
    def scrape_category(self, category_url):
        """Scrape all books in a specific category and save them."""
        self.categories.get_books_list(category_url)
        
        category_data = Category()
        for book_info in self.categories.category_books:
            book_obj = Book(book_info, self.categories.name)
            book_obj.get_book()
            category_data.append_to_init(book_obj)
        
        category_data.to_csv()
        category_data.reset_all_lists()
        self.categories.category_books = []

if __name__ == "__main__":
    scraper = BookScraper()
    scraper.scrape_all_categories()
    print("Scraping is now completed")
