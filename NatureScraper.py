import requests
import os, re
from datetime import datetime
from bs4 import BeautifulSoup
import pdfkit

from typing import List, Dict


class Scraper:
    def __init__(self):
        self.base_url = 'https://www.nature.com'

    def extract_nature_articles(self, start_date, end_date, title_keyword: str, save_pdf: bool=False, pdf_dir: str='.') -> List:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        search_url = '{base_url}/search?title={title_keyword}&order=date_asc&date_range={start_yr}-{end_yr}&journal=nature&article_type=news'.format(base_url=self.base_url,
                                                                                                                                                    title_keyword=title_keyword,
                                                                                                                                                    start_yr=start_dt.year,
                                                                                                                                                    end_yr=end_dt.year)
        soup = self.retrieve_url(search_url)
        all_atags = soup.find_all('a', {'data-track-action': 'view article'})

        if len(all_atags) == 0:
            print('No articles found')
            return []

        filtered_ids = [False] * len(all_atags)

        # filter titles
        all_titles = [atag.get_text().lower() for atag in all_atags]
        regex_title = re.compile('(daily briefing)|(podcast)|(backchat)')
        for i in range(len(all_titles)):
            if len(regex_title.findall(all_titles[i])) == 1:
                filtered_ids[i] = True

        # filter dates
        all_dates = [datetime.strptime(tag['datetime'], '%Y-%m-%d') for tag in soup.find_all('time', {'itemprop': 'datePublished'})]
        for i in range(len(all_dates)):
            if all_dates[i] < start_dt or all_dates[i] > end_dt:
                filtered_ids[i] = True

        atags = [all_atags[i] for i in range(len(all_atags)) if not filtered_ids[i]]

        articles = []
        for atag in atags:
            articles.append(self.parse_page(self.base_url + atag['href']))

        # sort articles
        articles_sorted = sorted(articles, key=lambda a: (a['Published Date'], a['Title']))
        if save_pdf:
            for article in articles_sorted:
                self.save_article_as_pdf(article, pdf_dir)

        return articles_sorted

    def retrieve_url(self, url: str) -> BeautifulSoup:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def parse_page(self, url: str) -> Dict:
        soup = self.retrieve_url(url)

        dt = datetime.strptime(soup.find('time', {'itemprop': 'datePublished'}).text, '%d %B %Y') # published date
        date_str = dt.strftime('%Y-%m-%d')

        title = soup.find('h1', {'itemprop': 'headline'}).text.strip() # title
        authors = [tag.text.strip() for tag in soup.find_all('a', {'data-test': 'author-name'})] # authors
        summary = soup.find('div', {'class': 'c-article-teaser-text'}).text.strip()

        article_div = soup.find('div', {'class', 'c-article-body'}) # content
        for r in article_div.find_all(attrs={'data-label': 'Related'}):
            r.extract()
        content_texts = []
        for tag in article_div.find_all('p'):
            text = tag.get_text().strip()
            if text:
                content_texts.append(text)

        return {
            'Title': title,
            'Author': authors,
            'Published Date': date_str,
            'Url': url,
            'Summary': summary,
            'Content': content_texts
        }

    def save_article_as_pdf(self, article, pdf_dir: str):
        if not os.path.exists(pdf_dir):
            os.mkdir(pdf_dir)

        cleaned_title = re.sub(r'[,.:;@#?!&$]+ \ *', " ", article['Title'], flags=re.VERBOSE).strip()
        pdf_path = os.path.join(pdf_dir, cleaned_title + '.pdf')
        print(f'Saving {pdf_path}')
        pdfkit.from_url(article['Url'], pdf_path)
