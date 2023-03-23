from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
from telegram.ext import (
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
    CommandHandler,
)
from alterbar_db import checkUserID, getAllEmployees, getEmployeeByID, Employee

USER_LIST = 0
USER_EDIT = 1


def constructEmployeesInlineKeybord():
    employees = getAllEmployees()
    buttons = []
    for current in employees:
        button_name = current.first_name + " " + current.last_name
        callback_data = "user_" + str(current.tg_user_id)
        buttons.append([InlineKeyboardButton(button_name, callback_data=callback_data)])
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
    employee_tg_id = int(query.data.split("user_")[1])
    employee = getEmployeeByID(employee_tg_id)
    employee_name = employee.first_name + " " + employee.last_name
    keyboard = [
        [InlineKeyboardButton("Rename", callback_data="rename_1")],
        [InlineKeyboardButton("Delete", callback_data="delete_1")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Edit user "{employee_name}"', reply_markup=reply_markup
    )
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
