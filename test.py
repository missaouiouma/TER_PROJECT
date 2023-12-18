import spacy
from bs4 import BeautifulSoup
import time

# Charger le modèle Spacy avec DBpedia Spotlight
nlp = spacy.blank('en')
nlp.add_pipe('dbpedia_spotlight')

# Lire le fichier XML
with open("Perseus_text_1999.02.0138.xml", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "xml")

# Initialisation des variables de contrôle de requête
total_requests = 0
requests_per_delay = 100
delay_duration = 60


# Fonction pour ajouter des balises <note> aux entités
def annotate_entities(paragraphs, lang):
    global total_requests
    for paragraph in paragraphs:
        if paragraph.text:
            try:
                doc = nlp(paragraph.text)
                for ent in doc.ents:
                    note = soup.new_tag("note")
                    note.string = " "
                    note['DBpedia'] = ent.text
                    note['Lang'] = lang
                    note['start'] = str(ent.start_char)
                    note['end'] = str(ent.end_char)
                    note['lien'] = ent._.dbpedia_raw_result['@URI']
                    note['type'] = ent._.dbpedia_raw_result.get('@types', '')
                    note['score'] = ent._.dbpedia_raw_result.get('@similarityScore', '')

                    paragraph.append(note)

                total_requests += 1  # Incrémenter le nombre total de requêtes
                print(f"Traitement du paragraphe {total_requests}")

                # Introduire une pause après un certain nombre de requêtes
                if total_requests % requests_per_delay == 0:
                    print(f"Pausing for {delay_duration} seconds...")
                    time.sleep(delay_duration)

            except Exception as e:
                print(f"Erreur lors du traitement de l'API pour le paragraphe : {paragraph.text[:30]}... Erreur : {e}")


# Annoter les paragraphes en anglais
annotate_entities(soup.find_all("p", {"lang": "en"}), "en")

nlp = spacy.blank('it')
nlp.add_pipe('dbpedia_spotlight')
# Annoter les paragraphes en italien
annotate_entities(soup.find_all("p", {"lang": "it"}), "it")

# Écrire les modifications dans un nouveau fichier XML
with open("Perseus_text_1999.02.0138.xml", "w", encoding="utf-8") as file:
    file.write(str(soup))
