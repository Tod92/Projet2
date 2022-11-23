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
            elif header.text == "Availability":
                available = element.find("td").text
                if available[0:8] == "In stock":
                    number_available = available[10:-11] #slice de la chaine de caractère pour isoler le nombre
                else:
                    number_available = "0"
        title = soup.find("h1")
        title = title.text
        product_description = soup.findAll("p")
        product_description = product_description[3].text #la description est contenue dans la 4e balise <p> de la page
        rating_list = ["One","Two","Three","Four","Five"]
        encart_droite = soup.find("div", {"class" : "col-sm-6 product_main"})
        for r in rating_list:
            tofind = "star-rating " + r
            if encart_droite.find("p", {"class" : tofind}):
                categoryreview_rating = r
                break
    else:
        pass #definir quoi faire si pas de connexion à la page web
    return [product_page_url,UPC,title,price_excl_tax,number_available,price_incl_tax,product_description,categoryreview_rating]


resultat = scrap_book(url)
print(resultat)
