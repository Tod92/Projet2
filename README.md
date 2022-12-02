# Projet 2 - Utilisez les bases de Python pour l'analyse de marché


Ce script Python a pout but de se connecter au site [books.toscrape.com](books.toscrape.com) et d'en éxtraire les données souhaitées via le process ETL *(Extract Transform Load)*


## Installation

* Installer Python 3.10.3 :
 https://www.python.org/downloads/release/python-3103/  
  _Compatibilité avec d'autres versions probable mais non testée_

* Télécharger et extraire le repository suivant depuis github :\
https://github.com/Tod92/Projet2

* Se positionner dans le répértoire où le repository a été extrait :\
  `..\Projet2-main\`

* Créer l'environnement virtuel :\
  `python -m venv env`

* Activer l'environnement virtuel :\
  `..\Projet2-main\env\Scripts\activate.bat`

* Installer les packages Python néçessaire à l'execution du script :\
  `(env)..\Projet2-main\pip install -r requirements.txt`

* Installation terminée. Désactivation de l'environnement virtuel :\
  `deactivate`

## Execution du Script

* L'environnement virtuel doit etre activé :\
  `..\Projet2-main\env\Scripts\activate.bat`

* Executer le script python :\
  `..\Projet2-main\python main.py`

* Attendre la fin de l'execution du script avec la mention :\
  `Traitement terminé`

* Penser à désactiver l'environnement virtuel :\
  `deactivate`

## Format des données

Une fois le script executé correctement, les fichiers suivants seront apparus le dossier de travail :
1. Un fichier CSV par catégorie d'ouvrages, nommé _nom_de_la_categorie_.csv, utilisant la virgule comme séparateur et contenant les informations suivantes, indiquées en en-tête du fichier :

* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

2. Un fichier JPG par ouvrage, correspondant à l'image de sa couverture présente sur le site.
A noter que pour des raisons techniques d'enregistrement des fichiers, le nom de ces fichiers images correspond au titre de l'ouvrage ayant subi les modifications suivantes :

* Les caractères spéciaux suivants ont été remplacés par le caractère "-" :

  * ’
  * '
  * :
  * .
  * &
  * *
  * /
  * \\
  * ?


* La longueur du titre a été tronquée à 30 caractères


## Historique

* 02/12/2022 : Finalisation projet et documentation
* 31/11/2022 : Mise en adéquation du code avec PEP 8
* 29/11/2022 : Phase 4 : téléchargement des images
* 28/11/2022 : Phase 3 : scraping complet
* 25/11/2022 : Phase 2 : scraping d'une categorie
* 23/11/2022 : Phase 1 : scraping d'un ouvrage
* 17/11/2022 : Démarrage du projet

## Credits
Projet réalisé par Thomas DERUERE\
Assisté par Idriss BEN GELOUNE (Mentor Openclassrooms)
