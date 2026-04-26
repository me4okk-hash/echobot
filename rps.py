import telebot
import os
import random
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

bot = telebot.TeleBot(TOKEN)

rps = ["Камінь", "Ножиці", "Папер"]

@bot.message_handler(commands=['start', 'help'])
def start_game(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Камінь")
    btn2 = types.KeyboardButton("Ножиці")
    btn3 = types.KeyboardButton("Папір")

    keyboard.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        "Обери: Камінь, Ножиці або Папер",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text in rps)
def play_game(message):
    user_choice = message.text
    bot_choice = random.choice(rps)

    if user_choice == bot_choice:
        result = "Нічия"

    elif (
        (user_choice == "Камінь" and bot_choice == "Ножиці") or
        (user_choice == "Ножиці" and bot_choice == "Папер") or
        (user_choice == "Папер" and bot_choice == "Камінь")
    ):
        result = "Ти переміг!"

    else:
        result = "Я переміг"

    bot.send_message(
        message.chat.id,
        f"Ти обрав: {user_choice}\n"
        f"Я обрав: {bot_choice}\n\n"
        f"{result}"
    )

@bot.message_handler(func=lambda message: True)
def error_message(message):
    bot.send_message(
        message.chat.id,
        "Натисни кнопку"
    )

if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()