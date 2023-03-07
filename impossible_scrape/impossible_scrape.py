import fitz
import re
from pdflatex import PDFLaTeX


DIGITIZED_FILE = 'materials/impossible.pdf'
OUTPUT_LATEX = 'output/impossible_scrape.tex'
OPENER_TEMPLATE = 'materials/opener.txt'
CLOSER_TEMPLATE = 'materials/closer.txt'

pages: list = []

# The columns of the impossible landscapes pdf are split at roughly x = 300, not in the center of the page.
CENTER_COLUMN = 300
PAGE_HEIGHT = 792

# This sorts spans of text, making sure stuff on the left side of the page goes first.
def page_sort(line_span: dict):
    value = line_span['bbox'][1]
    if line_span['bbox'][0] > CENTER_COLUMN:
        value += PAGE_HEIGHT
    return value

with fitz.open(DIGITIZED_FILE) as doc:
    for page in doc.pages(123,132,1):
        text_page = page.get_textpage()
        test_json = text_page.extractJSON()
        text_dicts = text_page.extractDICT()
        line_spans: list = []
        for tb in text_dicts['blocks']:
            for line in tb['lines']:
                raw_line_spans = line['spans']
                for i, spans in enumerate(raw_line_spans):
                    line_text = spans['text']
                    line_text = re.sub("\.$", ".\n\n", line_text)
                    line_text = re.sub("\$", "\\\$", line_text)
                    line_text = re.sub("\%", "\\%", line_text)
                    line_text = re.sub("’", "\'", line_text)
                    line_text = re.sub("(\w+)(-)$", r'\1', line_text)
                    line_text = re.sub("(\w+)(-)$", r'\1', line_text)
                    line_text = re.sub("\n\n", '', line_text)
                    line_text = re.sub("[а-яА-Я]+", '[Russian Word]', line_text)
                    line_text = re.sub("−", '-', line_text)
                    # Merge Headings if this and previous were size 18. (Some headings are formatted weirdly, and so are spread accross spans.)
                    if i > 0 and raw_line_spans[i - 1]['size'] == 18 and spans['size'] == 18:
                        line_spans[-1]['text'] += line_text
                    else:
                        # Otherwise just add the line as normal.
                        line_spans.append(dict(text=line_text, font=spans['font'], size=spans['size'], bbox=spans['bbox']))
        sorted_line_spans = sorted(line_spans, key=page_sort)
        pages.append(sorted_line_spans)

# Read in the text from file to open the latex document with.
with open(OPENER_TEMPLATE, 'r', encoding='utf-8') as opener:
    opener_text = opener.read()
# Read in the text from file to close the latex document with.
with open(CLOSER_TEMPLATE, 'r', encoding='utf-8') as closer:
    closer_text = closer.read()
# Open / create the tex file we will rewriting the impossible landscapes pdf data to.
file = open(OUTPUT_LATEX, 'w', encoding="utf-8")


first_chapter = True
file.write(opener_text)
for page in pages:
    for i, text in enumerate(page):
        match text['size']:
            # Normal Text
            case num if 9 <= num <= 12:
                file.write(f"{text['text']}")
            # Weird red text at start of chapter.
            case 11.0:
                file.write(f"{text['text']}")
            # Subsection heading
            case 14.0:
                file.write(f"\n\subsection{{{text['text']}}}\n")
            # OPINT
            case 15.0:
                file.write(f"\n\subsubsection{{{text['text']}}}\n")
            # Section Heading
            case 18.0:
                file.write(f"\n\section{{{text['text']}}}\n")
            # Chaper Heading
            case 36.0:
                if first_chapter:
                    file.write(f"\n\chapter{{{text['text']}}}\n\\begin{{multicols}}{{2}}\n")
                    first_chapter = False
                else:
                    file.write(f"\end{{multicols}}\n\chapter{{{text['text']}}}\n\\begin{{multicols}}{{2}}\n")
    # I want the latex pages to number the same as the orginal pdf, so I force a new page at the end of each read page.
    file.write("\\newpage\n")
file.write(closer_text)
file.close() 

pdfl = PDFLaTeX.from_texfile(OUTPUT_LATEX)
pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)