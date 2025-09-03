# pip install requests beautifulsoup4 selenium webdriver-manager

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"

def fetch_html(url: str) -> str :
    resp = requests.get(url, timeout=10)
    resp.raise_for_status() # 문제가 있으면 예외 발생 
    return resp.text

def parse_quotes(html, page_url) : 
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # 한 개의 명언 블록 :
    for q in soup.select("div.quote") : 
        text_el = q.select_one("span.text").strip("“”\"'")
        author_el = q.select_one("small.author")
        tag_els = q.select("a.tag")

        if not text_el or not author_el :
            continue

        text = text_el.get_text(strip=True)
        author = author_el.get_text(strip= True)
        tags = []
        for t in tag_els : 
            if tag_els :
                tags.append( t.get_text(strip=True) )
        results.append( {'quote' : text, 'author' : author , 'tags' : tags, 'source_url' : page_url } )
    return results

html = fetch_html(BASE_URL)
parse_quotes(html, BASE_URL)
