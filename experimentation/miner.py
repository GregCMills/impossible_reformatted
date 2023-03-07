from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from pdfminer.layout import LTChar

page_elements = []
text = ''

for page_layout in extract_pages('impossible.pdf', page_numbers=[313]):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):                        
                        font = character.fontname
                        font_size = character.size
            page_elements.append({'type': 'text','element': element.get_text(), 'font':font, 'font_size': font_size})
        else:
            page_elements.append({'type': 'unknown', 'element': element, 'font': 'Not Text', 'font_size': 'Not Text'})

for pe in page_elements:
    if pe['type'] == 'text':
        text += pe['element']


with open('impossible_scrape.txt', 'w') as f:
    f.write(text)
    # f.write(pmage_elements)