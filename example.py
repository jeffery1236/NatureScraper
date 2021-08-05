from NatureScraper import Scraper

scraper = Scraper()
articles = scraper.extract_nature_articles('2020-02-07', '2020-02-12', 'coronavirus', save_pdf=True, pdf_dir='./saved_articles')

# articles is a list of dictionaries with the following fields
# {
#     'Title': str,
#     'Author': List[str],
#     'Published Date': str,
#     'Url': str,
#     'Summary': str,
#     'Content': List[str]
# }

print(articles)
