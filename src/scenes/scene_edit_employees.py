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

USER_LIST, EDIT_OR_ADD, USER_EDIT = range(3)


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
    keyboard = [
        [InlineKeyboardButton("Add user", callback_data="add_user")],
        [InlineKeyboardButton("Edit users", callback_data="edit_user")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "What do you want to do?"
    if update.message:
        if not checkUserID(update.message.from_user.id):
            return None
        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(message, reply_markup=reply_markup)
    return EDIT_OR_ADD


async def user_list_to_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    reply_markup = constructEmployeesInlineKeybord()
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
            EDIT_OR_ADD: [
                CallbackQueryHandler(user_list_to_edit, pattern="^edit_user$"),
                CallbackQueryHandler(cancel, pattern="^back$"),
            ],
            USER_LIST: [
                CallbackQueryHandler(edit_user, pattern="^user_"),
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            USER_EDIT: [
                CallbackQueryHandler(user_list_to_edit, pattern="^back$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
