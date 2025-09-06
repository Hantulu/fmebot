import os
import requests
from bs4 import BeautifulSoup
import telebot
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ID получателя (можно захардкодить, можно хранить где-то ещё)
VIKA_ID = None  

# ======= Функции =======

def get_meme():
    URL = 'https://www.memify.ru/highfive/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    post = soup.find('div', class_='infinite-item card')
    meme = post.find('img')
    return meme['src'] if meme else None


def send_meme():
    if VIKA_ID:
        meme_url = get_meme()
        if meme_url:
            bot.send_photo(
                VIKA_ID,
                meme_url,
                "Вот мем на сегодня. <b>От Скотча — Я тебя очень сильно люблю ❤️</b>",
                parse_mode="html"
            )

# ======= Команды =======

@bot.message_handler(commands=["start"])
def start(message):
    global VIKA_ID
    VIKA_ID = message.chat.id
    bot.send_message(
        VIKA_ID,
        "Привет, Вика 🌸. Скотч тебя очень сильно любит ❤️ "
        "Я буду каждый день отправлять тебе новый мем 🥰"
    )
    send_meme()  # сразу присылаем мем при старте

# ======= Flask маршруты =======

@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

# ======= Планировщик =======
scheduler = BackgroundScheduler()
scheduler.add_job(send_meme, "interval", hours=5)  # каждые 5 часов
scheduler.start()

# ======= Точка входа =======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
