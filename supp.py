from bs4 import BeautifulSoup

# Charger le contenu du fichier XML
with open("Perseus_text_1999.02.0138.xml", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "xml")

# Trouver et supprimer toutes les balises <note> avec des annotations Wikidata
com=0
for note in soup.find_all('note', {'Wikidata': True}):
    note.decompose()
    com=com+1
    print(com)

# Sauvegarder le contenu modifié dans un nouveau fichier
with open("Perseus_text_1999.02.0138.xml", "w", encoding="utf-8") as file:
    file.write(str(soup))