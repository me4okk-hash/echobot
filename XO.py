import telebot
import os
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

bot = telebot.TeleBot(TOKEN)

board = [" "] * 9
player_symbol = "X"
bot_symbol = "O"


def create_board():
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    buttons = []

    for i in range(9):
        text = board[i]

        if text == " ":
            text = "⬜"

        button = types.InlineKeyboardButton(
            text=text,
            callback_data=str(i)
        )

        buttons.append(button)

    keyboard.add(*buttons)

    return keyboard


def check_winner(symbol):
    win_positions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for pos in win_positions:
        if (
            board[pos[0]] == symbol and
            board[pos[1]] == symbol and
            board[pos[2]] == symbol
        ):
            return True

    return False


@bot.message_handler(commands=['start'])
def start_game(message):
    keyboard = types.InlineKeyboardMarkup()

    btn_x = types.InlineKeyboardButton(
        "X",
        callback_data="X"
    )

    btn_o = types.InlineKeyboardButton(
        "O",
        callback_data="O"
    )

    keyboard.add(btn_x, btn_o)

    bot.send_message(
        message.chat.id,
        "Обери крестик/нулик",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data in ["X", "O"])
def choose_symbol(call):
    global player_symbol
    global bot_symbol
    global board

    board = [" "] * 9

    player_symbol = call.data

    if player_symbol == "X":
        bot_symbol = "O"
    else:
        bot_symbol = "X"

    bot.send_message(
        call.message.chat.id,
        "Гра почалась",
        reply_markup=create_board()
    )


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def play_game(call):
    index = int(call.data)

    if board[index] != " ":
        return

    board[index] = player_symbol

    if check_winner(player_symbol):
        bot.edit_message_text(
            "Ти переміг!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_board()
        )
        return

    if " " not in board:
        bot.edit_message_text(
            "Нічия",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_board()
        )
        return
    for i in range(9):
        if board[i] == " ":
            board[i] = bot_symbol
            break

    if check_winner(bot_symbol):
        bot.edit_message_text(
            "Бот переміг!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_board()
        )
        return

    if " " not in board:
        bot.edit_message_text(
            "Нічия",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_board()
        )
        return

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_board()
    )


if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()
