import os
import pandas as pd
import urllib.request
import re

class Category:

    def __init__(self):
        self.products_page_url = []
        self.upc = []
        self.titles = []
        self.prices_including_tax = []
        self.prices_excluding_tax = []
        self.number_available = []
        self.products_description = []
        self.category = []
        self.reviews_rating = []
        self.images_url = []
    
    def append_to_init(self, data):
        self.products_page_url.append(data.product_page_url)
        self.upc.append(data.upc)
        self.titles.append(data.title)
        self.prices_including_tax.append(data.price_including_tax)
        self.prices_excluding_tax.append(data.price_excluding_tax)
        self.number_available.append(data.number_available)
        self.products_description.append(data.product_description)
        self.category.append(data.category)
        self.reviews_rating.append(data.reviews_rating)
        self.images_url.append(data.image_url)
    
    def to_csv(self):
        datas = {
        'products_page_url': self.products_page_url,
        'upc': self.upc,
        'titles': self.titles,
        'prices_excluding_tax': self.prices_excluding_tax,
        'prices_including_tax': self.prices_including_tax,
        'number_available': self.number_available,
        'products_description': self.products_description,
        'category': self.category,
        'reviews_rating': self.reviews_rating,
        'images_url': self.images_url
        }

        """results folder creation and csv removal if it already exists"""
        subfolder = os.path.join("results", self.category[0])
        os.makedirs(subfolder, exist_ok=True)
        if os.path.exists(os.path.join(subfolder, f"{self.category[0]}.csv")):
            os.remove(os.path.join(subfolder, f"{self.category[0]}.csv"))
            print(f"le fichier {self.category[0]} a été suppr")

        """pandas dataframe and proper encoding"""
        dataframe = pd.DataFrame(datas)
        dataframe.to_csv(os.path.join(subfolder, f"{self.category[0]}.csv"), index=False, sep=',', encoding='utf-8-sig')

        """titles modification"""
        for title in range(len(self.titles)):
            img_title = (re.sub("[':,;!#*?/.-]", '', self.titles[title])).replace(" ", "_").replace('"', '')
            self.titles[title] = img_title
        """path attribution for each images with urllib.request"""
        for img in range(len(self.images_url)):
            path = subfolder + "/" + self.titles[img] + ".jpg"
            urllib.request.urlretrieve(self.images_url[img], path)
    
    def reset_all_lists(self):
        for attr, value in self.__dict__.items():
            if isinstance(value, list):
                value.clear()
    
