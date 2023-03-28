from alterbar_settings import settings
from telegram.ext import ApplicationBuilder, CommandHandler
from scenes import scene_start
from scenes import scene_edit_users
from scenes import scene_edit_menu


def startTelegramBot():
    tg = ApplicationBuilder().token(settings.telegram_token).build()
    tg.add_handler(CommandHandler("start", scene_start.start))
    tg.add_handler(scene_edit_users.returnHandler())
    tg.add_handler(scene_edit_menu.returnHandler())
    tg.run_polling()
