import telebot
from flask import Flask
from threading import Thread
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

def run_server():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot hoạt động rồi nhé!")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"Bạn nói: {message.text}")

if __name__ == "__main__":
    keep_alive()

    try:
        bot.infinity_polling(skip_pending=True, timeout=20)
    except Exception as e:
        print("Lỗi:", e)
