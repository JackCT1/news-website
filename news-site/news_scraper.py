from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup
import psycopg2

STORY_ANCHOR_TAG_CLASS = "ssrcss-its5xf-PromoLink exn3ah91"


def get_html(url):
    page = urlopen(url)
    html_bytes = page.read()
    html_doc = html_bytes.decode("utf_8")
    return html_doc


def parse_stories_bs(domain_url, html, stories):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all("a", class_=STORY_ANCHOR_TAG_CLASS)
    for tag in tags:
        print(tag.span.p.span.string)
        print(tag.get("href"))
        title = tag.span.p.span.string
        url = domain_url + tag.get("href")
        if title and url:
            stories.append(
                {
                    "created_at": datetime.now(),
                    "id": len(stories) + 1,
                    "score": 0,
                    "title": title,
                    "updated_at": datetime.now(),
                    "url": url,
                }
            )


if __name__ == "__main__":
    bbc_url = "http://bbc.co.uk"
    bbc_html_doc = get_html(bbc_url)
    parse_stories_bs(bbc_url, bbc_html_doc)
