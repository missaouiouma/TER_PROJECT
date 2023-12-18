from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time

def translate_large_text(text, translator, char_limit=5000, max_retries=5):
    translated_text = ""
    while text:
        if len(text) > char_limit:
            split_position = text.rfind(" ", 0, char_limit)
            if split_position == -1:
                split_position = char_limit
        else:
            split_position = len(text)

        segment = text[:split_position]
        retries = 0
        while retries < max_retries:
            try:
                translated_segment = translator.translate(segment)
                translated_text += translated_segment
                text = text[split_position:].lstrip()
                break  # Break out of the retry loop if successful
            except Exception as e:
                retries += 1
                time.sleep(1)  # Wait a bit before retrying
                if retries == max_retries:
                    raise Exception(f"Failed to translate after {max_retries} attempts. Last error: {e}")
    return translated_text


with open('phi0978.phi001.perseus-lat2.xml', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'xml')

# Créer un objet de traduction
translator = GoogleTranslator(source='latin', target='english')
translator_it = GoogleTranslator(source='latin', target='italian')

# Parcourir et traduire les paragraphes
com=1
for paragraph in soup.find_all('p'):
    if paragraph.text:
        #english
        translated_text = translate_large_text(paragraph.text, translator)
        new_paragraph_en = soup.new_tag('p', lang='en')
        new_paragraph_en.string = translated_text
        # Insertion du par traduit apres l'original
        paragraph.insert_after(new_paragraph_en)

        # italian
        translated_text_it = translate_large_text(paragraph.text, translator_it)
        new_paragraph_it = soup.new_tag('p', lang='it')
        new_paragraph_it.string = translated_text_it
        #inserer  apres  anglais
        new_paragraph_en.insert_after(new_paragraph_it)
        print(com)
        com=com+1

# Sauvegarder les modifs
with open('phi0978.phi001.perseus-lat2.xml', 'w', encoding='utf-8') as file:
    file.write(str(soup))
