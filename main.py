import requests
import csv
from bs4 import BeautifulSoup

Base_url = "http://books.toscrape.com/"
Base_url_catalogue = "http://books.toscrape.com/catalogue/"
Csv_header = ["product_page_url", "UPC", "title", "price_incl_tax",
              "price_excl_tax", "number_available", "product_description",
              "categoryreview_rating", "image_url"]


def url_to_soup(url):
    """
    se connecte à l'url et renvoi un objet bs4.BeautifulSoup contenant tout le
    code html de la page
    """
    # "lxml" pour evite un message d'avertissement de bs4 à l'execution du code
    response = requests.get(url, "lxml")
    # Ne va pas plus loin si la connexion à la page web ne fonctionne pas
    if response.ok:
        # Correction encodage pour les caractères s'afficheant mal
        response.encoding = response.apparent_encoding
        # Recuperation du html de la page web dans la variable soup
        soup = BeautifulSoup(response.text, features="html.parser")
    else:
        print("PB connexion à : " + url)
        soup = None
    return soup


def url_remove_end(url):
    """
    Fonction qui va modifer l'url reçue en entrée en retirant "index.html" ou
    "page-x.html"
    Renvoie la même url qu'en entrée si aucun des deux termes n'est trouvé
    """
    lenght = url.find("index.html")
    if lenght != -1:
        return url[:lenght]
    lenght = url.find("page-")
    if lenght != -1:
        return url[:lenght]
    return url


def scrap_index(url):
    """
    Url en entree doit etre la page d'accueil de booktoscrap contenant la liste
    des categories de livres
    Return une liste des urls de toutes les categories de livres et une liste
    des noms des categories
    """
    soup = url_to_soup(url)
    # On se concentre uniquement sur la liste de categories a gauche de la page
    soup = soup.find("div", {"class": "side_categories"})
    categories = soup.findAll("li")
    list_categories_urls = []
    list_categories_names = []
    for category in categories:
        category_url = Base_url + category.a["href"]
        list_categories_urls.append(category_url)
        category_name = category.a.text
        category_name = category_name.strip()
        list_categories_names.append(category_name)
    # Suppression de la premiere entrée de la liste qui ne correspond pas à une
    # vraie categorie ("Books")
    list_categories_urls = list_categories_urls[1:]
    list_categories_names = list_categories_names[1:]

    return list_categories_urls, list_categories_names


def scrap_category(url):
    """
    url en entrée doit etre le lien de la page d'une categorie
    return une liste des urls de tous les livres de la catégorie
    """

    soup = url_to_soup(url)
    # Recuperation de la liste des balises article correspondant à chaque livre
    # de la page
    articles = soup.findAll("article", {"class": "product_pod"})
    list_books_urls = []
    for article in articles:
        book_url = Base_url_catalogue + article.a["href"]
        # Nettoyage de l'url en retirant tous les "/.."
        book_url = book_url.replace("/..", "")
        list_books_urls.append(book_url)
    # Recherche la présence du bouton "next" pour savoir si une page suivante
    # contenant d'autres livres est presente
    nextpage = soup.find("li", {"class": "next"})
    if nextpage:
        url_next = url_remove_end(url) + nextpage.a["href"]
        # La fonction s'invoque de manière recursive pour la page suivante
        list_next = scrap_category(url_next)
        list_books_urls += list_next

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
    # Creation d'un liste "tableau" contenant tous les tableaux de la page
    tableau = soup.findAll("tr")
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
                # Slice de la chaine de caractère pour isoler le nombre
                number_available = available[10:-11]
            else:
                number_available = "0"
    title = soup.find("h1")
    title = title.text
    product_description = soup.findAll("p")
    # La description est contenue dans la 4e balise <p> de la page
    product_description = product_description[3].text
    rating_list = ["One", "Two", "Three", "Four", "Five"]
    encart_droite = soup.find("div", {"class": "col-sm-6 product_main"})
    for r in rating_list:
        tofind = "star-rating " + r
        if encart_droite.find("p", {"class": tofind}):
            categoryreview_rating = r
            break
    encart_gauche = soup.find("div", {"class": "col-sm-6"})
    image_url = Base_url + encart_gauche.img["src"]
    image_url = image_url.replace("/..", "")
    dowload_image(title, image_url)
    return [product_page_url, UPC, title, price_excl_tax, number_available,
            price_incl_tax, product_description, categoryreview_rating,
            image_url]


def clean_title(texte):
    """
    transforme les caractères speciaux d'un string en -
    """
    # str1 liste les caractères spéciaux à remplacer
    str1 = "\':.&*/\\\"?"
    str2 = ""
    # Boucle pour que str soit de la même longueur que str1 afin d'en faire une

    for c in str1:
        str2 += "-"
    mytable = texte.maketrans(str1, str2)
    texte_clean = texte.translate(mytable)

    return texte_clean


def dowload_image(title, image_url):
    """
    Va telecharger l'image au format.jpg dans le dossier courant
    le nom du fichier sera détérminé par title
    """
    response = requests.get(image_url)
    if response.ok:
        title = clean_title(title)
        title += ".jpg"
        with open(title, "wb") as file:
            file.write(response.content)


def ajout_csv(liste, file_name):
    """
    En entrée : une liste d'elements qui seront ecrits dans une ligne du
    fichier csv, séparés par une virgule et le nom du fichier csv dans lequel
    ajouter la ligne
    """
    with open(file_name, "a", newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(liste)


def main():
    list_categories_urls, list_categories_names = scrap_index(Base_url)
    for n in range(len(list_categories_names)):
        cat_url = list_categories_urls[n]
        cat_name = list_categories_names[n]
        file_name = cat_name + ".csv"
        print("Scraping category : " + cat_name)
        with open(file_name, "w", newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(Csv_header)
        list_books_urls = scrap_category(cat_url)
        for book_url in list_books_urls:
            print("Scraping book : " + book_url)
            ajout_csv(scrap_book(book_url), file_name)
    print("Traitement terminé")


if __name__ == '__main__':
    main()
