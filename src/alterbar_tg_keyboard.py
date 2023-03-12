from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton

main_buttons = (
    "New order",
    "My orders",
    "All orders",
    "Edit menu",
    "Close day",
)


def __createKeyboard(buttons: tuple):
    kbd = ReplyKeyboardMarkup(row_width=3)
    kbd.add(*buttons)
    return kbd


main_keyboard = __createKeyboard(main_buttons)
