from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import InlineKeyboardButton

main_buttons = [
    "New order",
    "My orders",
    "All orders",
    "Edit menu",
    "Close day",
]


def __createKeyboard(buttons: list):
    kbd = ReplyKeyboardMarkup(row_width=3)
    kbd.add(*buttons)
    return kbd


def createInlineKeyboard(buttons: list):
    kbd = InlineKeyboardMarkup()
    for cur in buttons:
        kbd.add(InlineKeyboardButton(text=cur, callback_data=cur))
    return kbd


main_keyboard = __createKeyboard(main_buttons)
