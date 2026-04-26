import telebot
import os
import random
import string
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    bot.reply_to(message, "Напиши число, і я сгенерую пароль на цю кількість символів!")

@bot.message_handler(func=lambda message: message.text.isdigit())
def generate_password(message):
    length = int(message.text)

    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    password = ''.join(random.choice(chars) for i in range(length))

    bot.send_message(message.chat.id, password)

@bot.message_handler(func=lambda message: True)
def error_message(message):
    bot.send_message(message.chat.id, 'Помилка, напиши число будь ласка!')

if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()