import telebot
from flask import Flask
from threading import Thread
import time

# --- CẤU HÌNH ---
# Hãy thay thế bằng Token bạn lấy từ BotFather
API_TOKEN = '8560870294:AAGCeIx2MAylVZtUwH0DwXM3E5Y20RyrCAY'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- PHẦN 1: SERVER ẢO (KEEP ALIVE) ---
@app.route('/')
def home():
    return "I'm alive! Bot đang hoạt động."

def run_http_server():
    # Chạy server trên port 8080 (hoặc port do Render cấp)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Chạy server Flask trong một luồng riêng biệt (thread)
    # để không chặn luồng chính của Bot
    t = Thread(target=run_http_server)
    t.start()

# --- PHẦN 2: LOGIC CỦA BOT ---

# Xử lý lệnh /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Tôi là bot chạy 24/24 đây.\nHãy thử chat gì đó xem.")

# Xử lý tin nhắn văn bản bất kỳ
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    phan_hoi = f"Bạn vừa nói: {message.text}"
    bot.reply_to(message, phan_hoi)

# --- PHẦN 3: CHẠY CHƯƠNG TRÌNH ---
if __name__ == '__main__':
    # 1. Kích hoạt server ảo trước
    keep_alive()
    
    # 2. Bắt đầu chạy Bot
    print("Bot đang khởi động...")
    try:
        # infinity_polling giúp bot tự kết nối lại nếu rớt mạng
        bot.infinity_polling() 
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")