import telebot
import os
import random
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

bot = telebot.TeleBot(TOKEN)

answers = [
    "Так",
    "Ні",
    "Можливо",
    "Скоріш за все",
    "Без сумнівів",
    "Мабуть пізніше",
]

@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.reply_to(message, 'Привіт! Я проста магічна куля! Надішли будь яке запитання я погадаю тобі!')

@bot.message_handler(func=lambda message: message.text.endswith("?"))
def magic_ball_answer(message):
    bot.send_message(
        message.chat.id,
        random.choice(answers)
    )


if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()