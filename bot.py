import telepot
import requests
from bs4 import BeautifulSoup
import time
import logging
import feedparser
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telepot.Bot('8667672105:AAELRl01QQRbbgVVzTfdi1u9khjGkxHbOZY')


REDDIT_FEED = 'https://www.reddit.com/r/CryptoCurrency/.rss'

def scrape_reddit():
    feed = feedparser.parse(REDDIT_FEED)
    new_messages = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        new_messages.append(f"{title} - {link}")

    return new_messages

def search_news():
    global interval
    while True:
        new_messages = scrape_reddit()
        if new_messages:
            for message in new_messages:
                bot.sendMessage('6834587572', message)
        time.sleep(interval)

def set_interval(update, context):
    global interval
    if len(context.args) == 0:
        update.message.reply_text("Bitte gib eine Zahl in Sekunden an: /setinterval <Sekunden>")
        return
    try:
        interval = int(context.args[0])
        update.message.reply_text(f"Das Zeitintervall wurde auf {interval} Sekunden gesetzt.")
    except ValueError:
        update.message.reply_text("Bitte gib eine gültige Zahl für das Intervall in Sekunden ein.")

def unknown(update, context):
    update.message.reply_text("Leider keine gültige eingabe. Zum Ändern des intervalls, nutze /interval <Sekunden>")

def start(update, context):
    chat_id = update.message.chat.id
    bot.sendMessage(chat_id, "Bot läuft!")

def main():
    print("Bot läuft...Nachrichten werden überprüft!")
    bot.sendMessage('6834587572','Der bot ist jetzt aktiv und läuft.')

    threading.Thread(target=search_news, daemon=True).start()

    bot.message_loop({
        'chat': start,
        '/setinterval': set_interval
    }, timeout=10)

    while True:
        time.sleep(10)

if __name__ == '__main__':
    main()