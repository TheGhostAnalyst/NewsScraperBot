Here’s a **detailed `README.md`** file for your **news scraper bot** project, complete with setup instructions, usage, and relevant details.

---

# **News Scraper Bot**

A **Python Telegram bot** that scrapes news articles from the **Punch Nigeria** website and sends them to your Telegram chat. The bot checks for new articles every 5 minutes and sends the latest updates with a brief preview of the content.

### Features:

* **Web Scraping**: Scrapes articles from the **Punch Nigeria** website using **BeautifulSoup**.
* **Telegram Integration**: Sends news updates via a Telegram bot using the **Telegram Bot API**.
* **Custom User-Agent & Proxy**: Uses a **random user-agent** and connects through **Tor (socks5 proxy)** to ensure anonymity.

---

## **Table of Contents**

* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [How It Works](#how-it-works)
* [License](#license)

---

## **Installation**

### 1. Clone the Repository:

Clone this repository to your local machine to get started:

```bash
git clone https://github.com/TheGhostAnalyst/NewsScraperBot.git
cd news-scraper-bot
```

### 2. Set Up a Python Virtual Environment:

It’s highly recommended to use a virtual environment to manage your dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies:

Install all the required dependencies using **`pip`** from the `requirements.txt`:

```bash
pip install -r requirements.txt
```

You may need to create the `requirements.txt` if it's not already included. You can generate it using:

```bash
pip freeze > requirements.txt
```

Here's the content of `requirements.txt`:

```
requests
beautifulsoup4
fake-useragent
python-telegram-bot
```

### 4. Set Up Tor Proxy:

This script uses **Tor** as a **proxy** to anonymize the web scraping process. Make sure you have **Tor** installed and running.

* **Install Tor** (if not already installed):

  * On Linux (Debian/Ubuntu):

    ```bash
    sudo apt-get install tor
    sudo service tor start
    ```
  * On macOS:

    ```bash
    brew install tor
    brew services start tor
    ```
  * On Windows:

    * Download and install **[Tor Browser](https://www.torproject.org/download/)**.
    * Start **Tor** as a service.

After installing, make sure your Tor proxy is running on the default address `127.0.0.1:9050`.

---

## **Configuration**

### 1. **Telegram Bot Token**:

To send messages via Telegram, you need a **Telegram bot token**.

* **Create a Telegram bot**:

  1. Open **Telegram** and search for the **BotFather**.
  2. Type `/newbot` and follow the prompts to create a bot.
  3. Copy the bot **API token**.

### 2. **Telegram Chat ID**:

To send the messages to a specific chat (you can use a group or personal chat), you'll need the **chat ID**.

* Send a message to your bot, then visit this URL in your browser to get your chat ID:

  ```
  https://api.telegram.org/bot<your_bot_token>/getUpdates
  ```

  Replace `<your_bot_token>` with the token you obtained earlier. The response will include your chat ID.

### 3. **Set Up Environment Variables**:

Store your **Telegram Bot Token** and **Chat ID** securely using environment variables. You can create a `.env` file with the following:

```
BOT_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
```

Make sure to replace the placeholders with your actual values.

---

## **Usage**

### 1. Run the Script:

Once everything is set up, you can run the bot by executing the Python script.

```bash
python3 bot.py
```

The script will start scraping news from the **Punch Nigeria** website and send the latest articles to your Telegram chat.

### 2. Interact with the Bot:

When you start the script, you’ll be prompted to hit **Enter** to begin scraping. The bot will:

* Fetch articles from the Punch website.
* Send the **article title**, **URL**, and a **brief preview** to your Telegram chat.
* Check for new articles every **5 minutes**.

### 3. Stop the Bot:

To stop the bot, you can interrupt the script (Ctrl+C).

---

## **How It Works**

1. **Web Scraping**:

   * The bot scrapes the **Punch Nigeria** website (`https://punchng.com/all-posts`) using the **`requests`** library and **`BeautifulSoup`** to parse the HTML.
   * It looks for `article` tags and extracts the **title** and **URL**.
   * If the article URL has not been seen before (tracked via the `seen_links` set), the bot fetches the article's full content.

2. **Sending News**:

   * Once the content is scraped, the bot sends a message to the configured **Telegram chat** using the **Telegram Bot API**.
   * The message includes the **article title**, the **URL**, a **timestamp**, and a **brief preview** of the article’s content.

3. **Tor Proxy**:

   * The bot uses a **Tor proxy** (configured via `requests` session) to anonymize the scraping process.
   * It uses **socks5h** proxy with the default Tor setup (`127.0.0.1:9050`).

---

## **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## **Contact**

* **Project Author**: [TheGhostAnalyst](https://github.com/TheGhostAnalyst)
* **Telegram**: @scaramouche_11

---

### ✨ Now you're all set up! Enjoy building your bot, and let me know if you need any further help!
