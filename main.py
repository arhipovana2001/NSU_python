import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from urllib.parse import urlparse

import bs4.element
import pandas as pd
import requests
from bs4 import BeautifulSoup


class MultiThreaderCrawler:

    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme,
                                         urlparse(self.seed_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=5)
        self.scraped_pages = set([])
        self.scraped_articles = list()
        self.crawl_queue = Queue()
        for i in range(1, 11):
            self.crawl_queue.put(self.seed_url + "page" + str(i) + "/")

    def parse_article(self, div: bs4.element.PageElement):
        username = div.find_next("a", {"class": "tm-user-info__username"})
        title = div.find_next("h2", {"class": "tm-title tm-title_h2"})
        views = div.find_next("span", {"class": "tm-icon-counter tm-data-icons__item"}).find_next("span")
        rating = div.find_next("span", {
            "class": "tm-votes-meter__value tm-votes-meter__value_positive tm-votes-meter__value_appearance-article tm-votes-meter__value_rating tm-votes-meter__value"})
        self.scraped_articles.append((username.text.strip(), rating.text, views.text, title.text))

    def parse_articles(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all("article", {"class": "tm-articles-list__item"})
        [self.parse_article(div) for div in articles]

    def scrape_info(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        web_page_paragraph_contents = soup('p')
        text = ''
        for para in web_page_paragraph_contents:
            if not ('https:' in str(para.text)):
                text = text + str(para.text).strip()
        return

    def post_scrape_callback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            self.parse_articles(result.text)
            self.scrape_info(result.text)

    def scrape_page(self, url):
        try:
            res = requests.get(url, timeout=(3, 30))
            return res
        except requests.RequestException as err:
            return

    def run_web_crawler(self):
        while True:
            try:
                target_url = self.crawl_queue.get(timeout=5)
                if target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    self.current_scraping_url = "{}".format(target_url)
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)

            except Empty:
                return
            except Exception as e:
                continue

    # def info(self):
    #     # print('\n Seed URL is: ', self.seed_url, '\n')
    #     # print('Scraped pages are: ', self.scraped_pages, '\n')
    #     return

    def get_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.scraped_articles, columns=["username", "rating", "views", "title"])


cc = MultiThreaderCrawler('https://habr.com/ru/flows/design/articles/')
cc.run_web_crawler()
df = cc.get_df()
# cc.info()
df["rating"] = df["rating"].astype(int)
print(df)
