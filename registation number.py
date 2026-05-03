from rich.console import Console
import os
import telebot

console = Console()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

user_numbers = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введiть номер телефону")


@bot.message_handler(func=lambda message: True)
def register_number(message):
    number = message.text

    if number.replace("+", "").isdigit():
        user_numbers[message.chat.id] = number
        bot.send_message(message.chat.id, "Номер телефону зареєстровано!")
        console.print(f"{message.chat.id}: {number}", style="green")
    else:
        bot.send_message(message.chat.id, "Неправильний номер телефону")
        console.print("Неправильний номер", style="red")


bot.polling()
