import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import time
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет, Вика. Скотч тебя очень сильно любит, поэтому я буду каждый день отправлять тебе новый мем')
    while True:
        URL = 'https://www.memify.ru/highfive/'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, ('html.parser'))

        post = soup.find('div', class_ = 'infinite-item card')
        meme = post.find('img')

   
        bot.send_photo(message.chat.id, f"{meme['src']}", f"Вот мем на сегодня. <b>От Скотча - Я тебя очень сильно люблю</b>", parse_mode='html' )
        time.sleep(43200)
bot.polling(none_stop=True)
