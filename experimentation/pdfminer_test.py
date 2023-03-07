from PyPDF2 import PdfReader

if __name__ == "__main__":
	reader = PdfReader("impossible.pdf")
	# number_of_pages = len(reader.pages)
	page = reader.pages[313]
	text = page.extract_text()

	with open('impossible_scrape.txt', 'w', encoding="utf-8") as f:
		f.write(text)