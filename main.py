import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/naked_197/index.html"

def scrap_book(url):
    """return liste contenant :
    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_description
    categoryreview_rating
    image_url"""

    product_page_url = url
    response = requests.get(url,"lxml") #"lxml" pour evite un message d'avertissement de bs4 à l'execution du code
    response.encoding = response.apparent_encoding #correction encodage pour les caractères s'afficheant mal
    if response.ok: #ne va pas plus loin si la connexion à la page web ne fonctionne pas
        soup = BeautifulSoup(response.text,features="html.parser") #recuperation du html de la page web dans la variable soup
        tableau = soup.findAll("tr") #creation d'un liste "tableau" contenant tous les tableaux de la page
        for element in tableau:
            header = element.find("th")
            if header.text == "UPC":
                UPC = element.find("td").text
            elif header.text == "Price (excl. tax)":
                price_excl_tax = element.find("td").text
            elif header.text == "Price (incl. tax)":
                price_incl_tax = element.find("td").text
        title = soup.find("h1")
        title = title.text
        product_description = soup.findAll("p")
        product_description = description[3].text #la description est contenue dans la 4e balise <p> de la page
    else:
        pass #definir quoi faire si pas de connexion à la page web
    return [product_page_url,UPC,title,price_excl_tax,price_incl_tax,product_description]


resultat = scrap_book(url)
print(resultat)
