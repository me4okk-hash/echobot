import telebot
import os
import re 
from dotenv import load_dotenv
from telebot import types
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))

class RegistationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()

reg_kb = types.ReplyKeyboardMarkup()
reg_btn = types.KeyboardButton('Реєстреція по пошті📰')
phn_btn = types.KeyboardButton('Реєстрація по телефону📱')
reg_kb.add(reg_btn, phn_btn)

cancel_kb = types.InlineKeyboardMarkup()
cancel_btn = types.InlineKeyboardButton('Скасувати', callback_data='cancel')
cancel_kb.add(cancel_btn)

remove_kb = types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        'Привіт! Натисни "Реєстрація" щоб отримувати спам на пошту/номер!',
        reply_markup=reg_kb
    )


@bot.message_handler(func=lambda message: message.text.startswith('Реєстреція'))
def start_email_registation(message):
    temp_msg = bot.send_message(
        message.chat.id,
        '⌛Оновлюємо інтерфейс...',
        reply_markup=remove_kb
    )
    
    bot.delete_message(message.chat.id, temp_msg.id)

    bot.set_state(message.from_user.id,
                  RegistationStates.waiting_for_email,
                  message.chat.id)
    
    bot.send_message(
        message.chat.id,
        'Чудово! Надішли мені адресу електронної пошти, на яку хочеш отримувати спам!',
        reply_markup=cancel_kb
    )

@bot.message_handler(state=RegistationStates.waiting_for_email)
def process_email(message):
    email = message.text
    email_pattern = r"^[\w\.-_]+@[\w\.\-_]+\.\w+$"

    if re.match(email_pattern, email):
        print(f'New email: {email}')
        with open('emails.txt', '+a') as file:
            file.write(email + '\n')
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(
            message.chat.id,
            'Дякую! Тепер спам буде надходити тобі регулярно! Натисни "Реєстрація" знову, якщо хочеш додати ще одну пошту!',
            reply_markup=reg_kb
        )
    else:
        bot.send_message(
            message.chat.id,
            'Це не схоже на адресу електронної пошти! Спробуй ще раз'
        )

@bot.message_handler(func=lambda message: message.text.startswith('Реєстрація по телефону'))
def start_phone_registration(message):
    temp_msg = bot.send_message(
        message.chat.id,
        '⌛Оновлюємо інтерфейс...',
        reply_markup=remove_kb
    )

    bot.delete_message(message.chat.id, temp_msg.id)

    bot.set_state(
        message.from_user.id,
        RegistationStates.waiting_for_phone,
        message.chat.id
    )

    bot.send_message(
        message.chat.id,
        'Введіть номер телефону на який буде приходити спам',
        reply_markup=cancel_kb
    )


@bot.message_handler(state=RegistationStates.waiting_for_phone)
def process_phone(message):
    phone = message.text

    if phone.replace("+", "").isdigit():
        with open ('phones.txt', '+a') as file:
            file.write(phone + '\n')

        bot.delete_state(message.from_user.id, message.chat.id)

        bot.send_message(
            message.chat.id,
            'Дякую, тепер на ваш номер регулярно буде надходити спам, натисни "Реєстрація" знову, якщо хочеш додати ще один номер',
            reply_markup=reg_kb
        )
    else:
        bot.send_message(
            message.chat.id,
            "Це не схоже на номер телефону! спробуй ще раз "
        )


@bot.callback_query_handler(lambda call: call.data == 'cancel')
def cancel_handler(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.send_message(
        call.message.chat.id,
        'Якщо передумаєш - натисни "Реєстрація📰" знову',
        reply_markup=reg_kb
    )
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()
