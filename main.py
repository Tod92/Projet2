import requests, csv
from bs4 import BeautifulSoup

Base_url = "http://books.toscrape.com/"
url = "http://books.toscrape.com/catalogue/naked_197/index.html"
Csv_header = ["product_page_url","UPC","title","price_incl_tax","price_excl_tax","number_available","product_description","categoryreview_rating","image_url"]

def url_to_soup(url):
    """
    se connecte à l'url et renvoi un objet bs4.BeautifulSoup contenant tout le code html de la page
    """
    soup = 0
    response = requests.get(url,"lxml") #"lxml" pour evite un message d'avertissement de bs4 à l'execution du code
    if response.ok: #ne va pas plus loin si la connexion à la page web ne fonctionne pas
        response.encoding = response.apparent_encoding #correction encodage pour les caractères s'afficheant mal
        soup = BeautifulSoup(response.text,features="html.parser") #recuperation du html de la page web dans la variable soup
    return soup



def scrap_category(url):
    """
    url en entrée doit etre le lien de la page d'une categorie
    return une liste des urls de tous les livres de la catégorie
    """
    articles = soup.findAll("article",{"class" : "product_pod"})
    list_books_urls = []
    for article in articles:
        book_url = Base_url + article.a["href"]
        list_books_urls.append(book_url)

    return list_books_urls

def scrap_book(url):
    """
    url en entrée doit etre le lien de la page d'un livre
    return liste contenant :
    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_description
    categoryreview_rating
    image_url
    """

    product_page_url = url
    soup = url_to_soup(url)
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
    encart_gauche = soup.find("div", {"class" : "col-sm-6"})
    image_url = Base_url + encart_gauche.img["src"]


    return [product_page_url,UPC,title,price_excl_tax,number_available,price_incl_tax,product_description,categoryreview_rating,image_url]

def ajout_csv(liste):
    """
    en entrée :[product_page_url,UPC,title,price_excl_tax,number_available,price_incl_tax,product_description,categoryreview_rating,image_url]
    """
    with open ("export.csv", "a",newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(liste)

def main():
    #on genère le fichier csv avec l'en-tête
    with open ("export.csv", "w",newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(Csv_header)
    resultat = scrap_book(url)
    ajout_csv(resultat)
    print(resultat)
    print("fichier export.csv généré")

if __name__ == '__main__':
    main()
