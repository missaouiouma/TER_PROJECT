import spacy
from bs4 import BeautifulSoup
import time

# Initialisation des variables de contrôle de requête
total_requests = 0
requests_per_delay = 200
delay_duration = 60


# Fonction pour ajouter des balises <note> aux entités
def annotate_dbpedia(paragraphs,nlp, lang):
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


def annotate_wikidata(paragraphs, nlp, lang):
    global total_requests
    for paragraph in paragraphs:
        if paragraph.text:
            try:
                doc = nlp(paragraph.text)
                for ent in doc.ents:
                    note = soup.new_tag("note")
                    note.string = " "
                    note['Wikidata'] = ent.text
                    note['Lang'] = lang
                    note['start'] = str(ent.start_char)
                    note['end'] = str(ent.end_char)
                    note['label'] = ent.label_
                    note['lien'] = ent._.url_wikidata if hasattr(ent._, 'url_wikidata') else " "
                    note['nerd_score'] = ent._.nerd_score if hasattr(ent._, 'nerd_score') else " "
                    paragraph.append(note)

                total_requests += 1
                print(f"Traitement du paragraphe {total_requests}")
                if total_requests % requests_per_delay == 0:
                    time.sleep(delay_duration)

            except Exception as e:
                print(f"Erreur : {e}")

# Charger les modèles Spacy pour DBpedia et Wikidata
"""""
nlp_dbpedia_en = spacy.blank('en')
nlp_dbpedia_en.add_pipe('dbpedia_spotlight')
nlp_dbpedia_it = spacy.blank('it')
nlp_dbpedia_it.add_pipe('dbpedia_spotlight')
"""
nlp_wikidata_en = spacy.load("en_core_web_sm")
nlp_wikidata_en.add_pipe("entityfishing")
nlp_wikidata_it = spacy.load("it_core_news_sm")
nlp_wikidata_it.add_pipe("entityfishing")

# Lire le fichier XML
with open("Perseus_text_1999.02.0138.xml", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "xml")

total_requests = 0
requests_per_delay = 200
delay_duration = 60

# Annoter les paragraphes avec DBpedia et Wikidata
#annotate_dbpedia(soup.find_all("p", {"lang": "en"}), nlp_dbpedia_en, "en")
#annotate_dbpedia(soup.find_all("p", {"lang": "it"}), nlp_dbpedia_it, "it")
annotate_wikidata(soup.find_all("p", {"lang": "en"}), nlp_wikidata_en, "en")
annotate_wikidata(soup.find_all("p", {"lang": "it"}), nlp_wikidata_it, "it")

# Écrire les modifications dans un nouveau fichier XML
with open("Perseus_text_1999.02.0138.xml", "w", encoding="utf-8") as file:
    file.write(str(soup))