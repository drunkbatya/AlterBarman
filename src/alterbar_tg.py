from alterbar_settings import settings
from alterbar_tg_security import checkUserID, setUserIDs
from telegram.ext import ApplicationBuilder, CommandHandler
from scenes import scene_start
from scenes import scene_edit_employees


def startTelegramBot():
    tg = ApplicationBuilder().token(settings.telegram_token).build()
    tg.add_handler(CommandHandler("start", scene_start.start))
    tg.add_handler(scene_edit_employees.returnHandler())
    setUserIDs()
    tg.run_polling()
