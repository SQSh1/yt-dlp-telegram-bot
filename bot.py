import os
from telebot import TeleBot
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "سلام! لینک یوتیوب بده تا فایل نهایی رو برات بفرستم (حداکثر 50MB).")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def handle_url(msg):
    url = msg.text
    filename = "/tmp/video.mp4"
    bot.send_message(msg.chat.id, "دانلود شروع شد...")
    os.system(f'yt-dlp -f "best[filesize<50M]" -o "{filename}" "{url}"')
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            bot.send_video(msg.chat.id, f)
        os.remove(filename)
    else:
        bot.send_message(msg.chat.id, "فایلی برای ارسال پیدا نشد یا از حد مجاز بزرگ‌تر بود.")

bot.infinity_polling()
