import telebot
import sqlalchemy
from alterbar_settings import settings
from alterbar_tg_keyboard import main_keyboard
from alterbar_tg_security import checkUserID, setUserIDs
from scenes.alterbar_scene_new_order import showSceneNewOrder

bot = telebot.TeleBot(settings.telegram_token)
__alterbar_tg_inline_callback = None


@bot.message_handler(commands=["start"])
def handle_start(msg):
    userID = msg.from_user.id
    if not checkUserID(userID):
        return False
    bot.send_message(msg.from_user.id, f"Hi, {userID}!", reply_markup=main_keyboard)


@bot.message_handler(content_types=["text"])
def text_handler(msg):
    if not checkUserID(msg.from_user.id):
        return False
    if msg.text == "New order":
        showSceneNewOrder(msg)


# types.py L 2729
@bot.callback_query_handler(lambda query: "_" in query.data)
def callbacks_inline_button(query):
    if not checkUserID(query.from_user.id):
        return False
    if __alterbar_tg_inline_callback:
        __alterbar_tg_inline_callback(query)


def startTelegramBot():
    setUserIDs()
    bot.infinity_polling()


def setTelegramInlineCallback(func):
    global __alterbar_tg_inline_callback
    __alterbar_tg_inline_callback = func
