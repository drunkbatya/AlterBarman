from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from alterbar_tg_security import checkUserID

main_keyboard_markup = ReplyKeyboardMarkup(
    [
        ["New order", "My orders", "All orders"],
        ["Edit menu", "Edit employees"],
    ]
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not checkUserID(update.message.from_user.id):
        return
    await update.message.reply_text("Hi!", reply_markup=main_keyboard_markup)
