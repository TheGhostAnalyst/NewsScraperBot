import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# ====== Telegram Config ======
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print("Telegram error:", e)

# ====== Scraper Config ======
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

url = "https://punchng.com/all-posts"
ua = UserAgent()
headers = {'User-Agent': ua.random}

seen_links = set()
separator = "=" * 80

def scrape_articles():
    session = requests.session()
    session.proxies.update(proxies)
    session.headers.update(headers)

    try:
        res = session.get(url, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        articles = soup.find_all('article')

        for article in articles:
            title_tag = article.find('a', href=True)
            if not title_tag:
                continue

            article_url = title_tag['href'].strip()
            if article_url in seen_links:
                continue
            seen_links.add(article_url)

            timestamp_tag = article.find('span', class_="post-date")

            # fetch article content
            resp = session.get(article_url, timeout=20)
            resp.raise_for_status()
            soup_article = BeautifulSoup(resp.text, "html.parser")

            content_div = soup_article.find('div', class_='post-content')
            if not content_div:
                continue

            paragraphs = content_div.find_all('p')
            seen_paragraphs = set()
            news_preview = []

            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and "Related News" not in text:
                    if text not in seen_paragraphs:
                        seen_paragraphs.add(text)
                        news_preview.append(text)

            # ====== Telegram Notify ======
            preview_text = "\n\n".join(news_preview[:1]) if news_preview else ''

            message = (
            f"📰 <b>{title_tag.text.strip()}</b>\n"
            f"{article_url}\n"
            f"🕒 {timestamp_tag.text.strip() if timestamp_tag else 'N/A'}\n\n"
            f"{preview_text}"
            )
            send_telegram(message)

            print(f"Sent to Telegram: {title_tag.text.strip()}")
            time.sleep(2)

    except Exception as e:
        print("Error:", e)


ask = input('Hit enter to start news scrape: ')
if ask == '':
    print('Checking for latest News......')
    scrape_articles()
    print("Done scraping now let me scan for you after every 5mins")

while True:
    print("Checking for new articles...\n")
    scrape_articles()
    print("Waiting 5 minutes...\n")
    time.sleep(300)
