import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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

def send_article_to_telegram(title, author, link, snippet):
    message = (
        f"⚽ <b>{title}</b>\n\n"
        f"👤 Author: {author}\n"
        f"🔗 {link}\n\n"
        f"{snippet}..."  # limit snippet size
    )
    send_telegram(message)

# Proxy settings for Tor
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Main URL to scrape
url = "https://www.goal.com/en-ng/news/1"  
ua = UserAgent()
headers = {'User-Agent': ua.random}

seen_links = set()

def scrape_football():
    session = requests.session()
    session.proxies.update(proxies)
    session.headers.update(headers)
    
    try:
        # Step 1: Fetch the main page
        res = session.get(url, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Step 2: Extract all 'a' links
        a_tags = soup.find_all('a', href=True)
        for a in a_tags:
            link = urljoin(url, a['href'])
            if 'lists' in link and link not in seen_links:
                seen_links.add(link)

        # Step 3: Visit each unique link
        for link in seen_links:
            try:
                resp = session.get(link, timeout=20)
                resp.raise_for_status()
                new_soup = BeautifulSoup(resp.text, "html.parser")

                article = new_soup.find('article')
                if article:
                    # Title
                    head_tag = "No title"
                    head = article.find('h1')
                    if head:
                        head_tag = head.text.strip()

                    # Author
                    author_name = "Unknown"
                    for a_tag in article.find_all('a', href=True):
                        if 'author' in a_tag['href']:
                            author_name = a_tag.text.strip()
                            break  

                    # Paragraphs
                    snippet_list = []
                    paragraphs = article.find_all('p')
                    for p in paragraphs[:2]:
                        sss = p.text.strip()
                        if sss:
                            snippet_list.append(sss)
                    snippet = "\n\n".join(snippet_list)

                    # Send to Telegram
                    send_article_to_telegram(head_tag, author_name, link, snippet)
                    print(f"✅ Sent to Telegram: {head_tag}")
                    time.sleep(2)
                else:
                    print(f"❌ No article found at {link}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching {link}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Start scraping
ask = input('Press ENTER to start football news: ')
if ask == '':
    print('Starting football news scraper...\n')
    # Directly start loop without extra scrape
    try:
        while True:
            print('Checking for new football news...\n')
            scrape_football()
            print('Waiting 5 minutes...\n')
            time.sleep(300)
    except KeyboardInterrupt:
        print("Script stopped by user.")
else:
    print("Didn't I tell you to hit ENTER?")

