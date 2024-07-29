import requests
from bs4 import BeautifulSoup
import json
import newspaper
from tqdm import tqdm
import logging
import argparse

class ArticleScraper:
    def __init__(self, newspapers_list, pages_limit, output_file):
        self.newspapers_list = newspapers_list
        self.pages_limit = pages_limit
        self.output_file = output_file
        self.articles = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"
        }

    def finding_ars(self):
        for newspaper in self.newspapers_list:
            if newspaper == "kaosenlared":
                self.scrape_kaosenlared(newspaper)
            elif newspaper == "prensarural":
                self.scrape_prensarural(newspaper)
            elif newspaper == "rebelion":
                self.scrape_rebelion(newspaper)
            elif newspaper == "telesurtv":
                self.scrape_telesurtv(newspaper)
        
        logging.info(f"\nFound {len(self.articles)} articles in {self.pages_limit} pages")
        return self.articles

    def scrape_kaosenlared(self, newspaper):
        page = 1
        while page <= self.pages_limit:
            try:
                logging.info(f"Searching articles on page number {page} [{newspaper}]")
                url = f"https://kaosenlared.net/opinion/page/{page}"
                r = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(r.content, 'html5lib')
                coverpage_news = soup.find_all("h3", class_="elementor-post__title")
                for item in tqdm(coverpage_news):
                    self.articles.append(item.a['href'])
                page += 1
            except Exception as e:
                logging.error(f"Error, details {str(e)}")
                page += 1

    def scrape_prensarural(self, newspaper):
        rubrique = 1
        while rubrique < 3:
            page = 0
            while page <= self.pages_limit - 1:
                try:
                    logging.info(f"Searching articles on page number {page} [{newspaper}]")
                    url = f"https://prensarural.org/spip/spip.php?rubrique{rubrique}&debut_articles={page}0#pagination_articles"
                    r = requests.get(url, headers=self.headers)
                    soup = BeautifulSoup(r.content, 'html5lib')
                    coverpage_news = soup.find_all("h3", class_="titre")
                    for item in tqdm(coverpage_news):
                        self.articles.append("https://prensarural.org/spip/" + item.contents[0].attrs['href'])
                    page += 1
                except Exception as e:
                    logging.error(f"Error, details {str(e)}")
                    page += 1
            rubrique += 1

    def scrape_rebelion(self, newspaper):
        page = 1
        while page <= self.pages_limit:
            try:
                logging.info(f"Searching articles on page number {page} [{newspaper}]")
                url = f"https://rebelion.org/categoria/territorios/espana/page{page}"
                r = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(r.content, 'html5lib')
                coverpage_news = soup.find_all("h3", class_="entry-title")
                for item in tqdm(coverpage_news):
                    self.articles.append(item.parent.attrs['href'])
                page += 1
            except Exception as e:
                logging.error(f"Error, details {str(e)}")
                page += 1

    def scrape_telesurtv(self, newspaper):
        try:
            logging.info(f"Searching articles page [{newspaper}]")
            url = "https://telesurtv.net//seccion/opinion"
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            coverpage_news = soup.find_all("div", class_="titopi")
            for item in tqdm(coverpage_news):
                self.articles.append("https://telesurtv.net/" + item.contents[1].attrs['href'])
        except Exception as e:
            logging.error(f"Error, details {str(e)}")

    def art_download(self, articles_found):
        data = {'articles': []}
        for item in tqdm(articles_found):
            article = newspaper.Article(item)
            article.download()
            try:
                article.parse()
            except Exception as e:
                logging.error(f"Error parsing article!!! Details: {str(e)}")
                continue

            if len(article.authors) == 0 and "prensarural" in article.url:
                try:
                    soup = BeautifulSoup(article.html, 'html5lib')
                    article.authors = soup.find_all("span")[1].string
                    article.publish_date = soup.find_all("span")[1].nextSibling
                except Exception as e:
                    logging.error(f"Error, details {str(e)}")

            elif len(article.authors) == 0 and "rebelion" in article.url:
                try:
                    soup = BeautifulSoup(article.html, 'html5lib')
                    article.authors = soup.find_all("span")[2].string
                    article.publish_date = soup.find_all("span")[3].string
                except Exception as e:
                    logging.error(f"Error, details {str(e)}")

            data['articles'].append({
                'Author': str(article.authors),
                'Title': str(article.title),
                'Publish Date': str(article.publish_date),
                'Text': str(article.text),
                'Url': str(article.url),
                'Meta': str(article.meta_description),
            })

        logging.info(f"Downloaded {len(data['articles'])} articles")
        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def run(self):
        articles_found = self.finding_ars()
        self.art_download(articles_found)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape articles from specified newspapers")
    parser.add_argument('--pages_limit', type=int, default=9999, help='Limit the number of pages to download')
    parser.add_argument('--output_file', type=str, default='/tmp/output.json', help='Path to the output JSON file')
    parser.add_argument('--newspapers', type=str, nargs='+', default=["rebelion"], help='List of newspapers to download from')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    scraper = ArticleScraper(args.newspapers, args.pages_limit, args.output_file)
    scraper.run()

