from NatureScraper import Scraper

scraper = Scraper()

articles = scraper.extract_nature_articles('2020-02-07', '2020-02-12', 'coronavirus', save_pdf=True)

titles = [a['Title'] for a in articles]
print(titles)
