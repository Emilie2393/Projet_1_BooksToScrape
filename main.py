from categories import Categories
from book import Book
from category import Category

if __name__ == "__main__":

    categories = Categories()
    categories.get_category_list()
    for category in categories.categories_url_list:
        categories.get_books_list(category)
        
        category_data = Category()
        for book in categories.category_books:
            final = Book(book, categories.name)
            final.get_book()
            category_data.append_to_init(final)
        category_data.to_csv()
        category_data.reset_all_lists()
        categories.category_books = []
