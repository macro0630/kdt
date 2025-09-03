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
        text_el = q.select_one("span.text")
        author_el = q.select_one("small.author")
        tag_els = q.select("a.tag")

        if not text_el or not author_el :
            continue

        text = text_el.get_text(strip=True).strip("“”\"'")
        author = author_el.get_text(strip= True)
        tags = []
        for t in tag_els : 
            if tag_els :
                tags.append( t.get_text(strip=True) )
        
        results.append( {'quote' : text, 'author' : author , 'tags' : tags, 'source_url' : page_url } )

    # 다음 페이지 링크 추출 (있을 수도 있고, 없을 수도 있다) 
    next_link = soup.select_one("li.next > a")
    next_url = None
    if next_link and next_link.has_attr("href") :
        from urllib.parse import urljoin
        next_url = urljoin(page_url, next_link['href'])
        
    return results, next_url
    
import time
def crawl_all(start_url) :
    url = start_url
    all_rows = [] 
    visited = set() # 순환 방지 

    # 이미 방문한 url이 아니면 데이터를 가져온다. 
    while url and url not in visited :
        visited.add(url)
        # 1. html코드를 문자열로 가져온다.
        html = fetch_html(url)
        # 2. 문자열에서 원하는 곳의 데이터를 가져온다. 
        rows, next_url = parse_quotes(html, url)
        all_rows.extend(rows)
        # 3. 접속을 빠르게 연속적으로 하면 공격의심받으니까, 쉬었다가 처리하도록 한다.
        time.sleep(1)
        url = next_url
    
    return all_rows

# 아래 함수만 실행하면 동작한다.
all_rows = crawl_all(BASE_URL)

# csv 형식으로 저장하는 함수 
def save_csv(rows, path='quotes.csv') :
    with open(path, 'w', newline='', encoding='utf-8') as f :
        writer = csv.writer(f)
        # csv 파일의 형식 : 첫번째 행은 컬럼의 이름이 와야한다. 
        writer.writerow( ['quote', 'author', 'tags', 'source_url' ] )
        for r in rows :
            writer.writerow( [ r['quote'] , r['author'], ' | '.join( r['tags'] ) , r['source_url'] ] )

# 변수에 있는 데이터를 파일로 저장한다. 
save_csv(all_rows)


# jsonl 형식으로 저장하는 함수
def save_jsonl(rows, path='quotes.jsonl') :
    with open(path, 'w', encoding='utf-8') as f :
        for r in rows :
            json.dump(r, f, ensure_ascii=False)
            f.write('\n')
            
# 변수에 있는 데이터를 파일로 저장한다.
save_jsonl(all_rows)






