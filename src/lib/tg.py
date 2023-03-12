import telebot
import sqlalchemy
from . import db
from .settings import settings
from .tg_keyboard import main_keyboard
from .tg_security import checkUserID

__bot = telebot.TeleBot(settings.telegram_token)


@__bot.message_handler(commands=["start"])
def handle_start(msg):
    userID = msg.from_user.id
    if not checkUserID(userID):
        return False
    __bot.send_message(msg.from_user.id, f"Hi, {userID}!", reply_markup=main_keyboard)


@__bot.message_handler(content_types=["text"])
def text_handler(msg):
    if not checkUserID(msg.from_user.id):
        return False
    if msg.text == "Employees":
        pass


def startTelegramBot():
    __bot.infinity_polling()
