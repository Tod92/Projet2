#livre choisi : http://books.toscrape.com/catalogue/naked_197/index.html

import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/naked_197/index.html"

response = requests.get(url)
if response.ok:
    print(response.text)


if __name__ == "__main__":
    main()
