import telebot
import sqlalchemy
from alterbar_settings import settings
from alterbar_tg_keyboard import main_keyboard
from alterbar_tg_security import checkUserID, setUserIDs
from alterbar_tg_scene_manager import SceneManager
from scenes.alterbar_scene_config import scenesInit

bot = telebot.TeleBot(settings.telegram_token)
scene_manager = SceneManager()


@bot.message_handler(commands=["start"])
def handle_start(msg):
    userID = msg.from_user.id
    if not checkUserID(userID):
        return False
    bot.send_message(msg.from_user.id, f"Hi, {userID}!", reply_markup=main_keyboard)


@bot.message_handler(content_types=["text"])
def text_handler(msg):
    userID = msg.from_user.id
    messageID = msg.id
    if not checkUserID(userID):
        return False
    scene_manager.clearUserSceneStack(userID)
    if msg.text == "New order":
        scene_manager.nextScene("new_order", userID, messageID)


# types.py L 2729
@bot.callback_query_handler(lambda query: "_" in query.data)
def callbacks_inline_button(query):
    if not checkUserID(query.from_user.id):
        return False
    scene_manager.inlineCallback(query)


def startTelegramBot():
    scenesInit()
    setUserIDs()
    bot.infinity_polling()
