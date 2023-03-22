from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
from telegram.ext import (
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
    CommandHandler,
)
from alterbar_tg_security import checkUserID

USER_LIST = 0
USER_EDIT = 1


def constructEmployeesInlineKeybord():
    buttons = [
        [InlineKeyboardButton(str(user), callback_data="user_" + str(user))]
        for user in range(10)
    ]
    buttons.append([InlineKeyboardButton("Back", callback_data="back")])
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = constructEmployeesInlineKeybord()
    if update.message:
        if not checkUserID(update.message.from_user.id):
            return None
        await update.message.reply_text("Edit users", reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.edit_message_text(text="Edit users", reply_markup=reply_markup)
    return USER_LIST


async def edit_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Rename", callback_data="rename_1")],
        [InlineKeyboardButton("Delete", callback_data="delete_1")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Edit user USER", reply_markup=reply_markup)
    return USER_EDIT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Done!")
    return ConversationHandler.END


def returnHandler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Edit employees$"), start)],
        states={
            USER_LIST: [
                CallbackQueryHandler(edit_user, pattern="^user_"),
                CallbackQueryHandler(cancel, pattern="^back$"),
            ],
            USER_EDIT: [
                CallbackQueryHandler(start, pattern="^back$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
