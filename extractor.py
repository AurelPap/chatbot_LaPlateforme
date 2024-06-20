import requests
from bs4 import BeautifulSoup
import json


''''
Ce Code permet de scrapper une page web
Sortie: fichier json contenant les infos de la page en question

'''

json_name = "data.json" #prf-var-tssr-technicien-systemes-reseaux
# URL du site web cible (changer en fct de la page a scrapper)
url = "https://laplateforme.io/prf-var-tssr-technicien-systemes-reseaux/"


response = requests.get(url)

#si succés
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    data = {}
    # Extraire le s titres
    title = soup.find("title").get_text()
    data['title'] = title

    # Extraire tous les paragraphes
    paragraphs = soup.find_all("p")
    paragraph_texts = [p.get_text() for p in paragraphs]
    data['paragraphs'] = paragraph_texts

    # Extraire les en-têtes
    headers = soup.find_all(['h1','span', 'div' 'h2', 'h3', 'h4', 'h5', 'h6'])
    header_texts = [header.get_text() for header in headers]
    data['headers'] = header_texts

    # Specifique d'une section du site
    try:
        laplateforme_definition = soup.find('div', {"class" : "gmail_default"})
        plate_text = laplateforme_definition.get_text()
        data['extra_paragraphs'] = plate_text
    except:
        print("No def")

    # Extraire les liens hypertextes
    links = soup.find_all('a', href=True)
    link_texts = [{"text": link.get_text(), "href": link['href']} for link in links]
    data['links'] = link_texts
    structured_data = json.dumps(data, indent=4, ensure_ascii=False)
    
    # données structurées (json)
    print(structured_data)
    with open(json_name, "w", encoding="utf-8") as json_file:
        json_file.write(structured_data)
else:
    print("Erreur lors de la requête :", response.status_code)
