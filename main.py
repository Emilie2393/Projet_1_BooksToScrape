import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('article')
    print(title)

with open('urls.csv', 'w') as file:
    file.write(str(title))

