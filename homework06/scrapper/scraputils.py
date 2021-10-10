import time
import requests
import typing as tp
from bs4 import BeautifulSoup


def extract_news(parser: BeautifulSoup,
                 url: str) -> tp.List[tp.Dict]:
    """ Extract news from a given web page """
    news_list = []

    news_table = parser.table.findAll('table')[1]

    user = news_table.select('.subtext')
    refs = news_table.select('.storylink')

    for user, ref in zip(user, refs):
        point = user.select('.score')
        point = int(point[0].text.split()[0]) if point != [] else 0

        author = user.select(".hnuser")
        author = author[0].text if author != [] else "anon"

        url_link = ref.get("href", '')
        url_link = url + url_link if url_link.startswith('item') else url_link
        title = ref.text

        comments = 0
        for i in user.findAll('a'):
            text = i.text
            if 'comment' in text:
                comments = int(
                    text.replace('\xa0', ' ').split(' ')[0]
                )

        news_list.append(
            {
                'author': author,
                'comments': comments,
                'points': point,
                'title': title,
                'url': url_link,
            }
        )

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    return parser.select('a.morelink')[0]['href']


def get_news(
        url: str = "https://news.ycombinator.com/newest",
        n_pages=1
):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        timeout = 0.01
        print("Collecting data from page: {}".format(url))
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f'got response {url}')
        except Exception:
            print(f'starting timeout {timeout}')
            time.sleep(timeout)
            timeout *= 1.1
            continue
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            news_list = extract_news(soup, url)
            next_page = extract_next_page(soup)
            url = "https://news.ycombinator.com/" + next_page
            news.extend(news_list)
            n_pages -= 1
    return news

