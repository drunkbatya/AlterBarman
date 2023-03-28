from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
from telegram.ext import (
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
    CommandHandler,
)
import alterbar_db

USER_LIST, EDIT_OR_ADD, USER_EDIT, USER_RENAME_DIALOG, USER_DELETE_DIALOG = range(5)


def constructEmployeesInlineKeybord(users) -> InlineKeyboardMarkup:
    buttons = []
    for current in users:
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
        if not alterbar_db.checkUserID(update.message.from_user.id):
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
    users = alterbar_db.getAllUsers()
    reply_markup = constructEmployeesInlineKeybord(users)
    await query.edit_message_text(text="Edit users", reply_markup=reply_markup)
    return USER_LIST


async def edit_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    action, user_tg_id = query.data.split("_")
    user_tg_id = int(user_tg_id)
    if action == "admintoggle":
        alterbar_db.toggleAdminByID(user_tg_id)
    user = alterbar_db.getUserByID(user_tg_id)
    user_name = user.first_name + " " + user.last_name
    admin_toggle_text = "Dismiss admin" if user.is_admin else "Make admin"
    keyboard = [
        [InlineKeyboardButton("Rename", callback_data="rename_" + str(user_tg_id))],
        [
            InlineKeyboardButton(
                admin_toggle_text, callback_data="admintoggle_" + str(user_tg_id)
            )
        ],
        [InlineKeyboardButton("Delete", callback_data="delete_" + str(user_tg_id))],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Edit user "{user_name}"', reply_markup=reply_markup
    )
    return USER_EDIT


async def rename_user_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_tg_id = int(query.data.split("rename_")[1])
    user = alterbar_db.getUserByID(user_tg_id)
    user_name = user.first_name + " " + user.last_name
    context.user_data["edit_user_user_id"] = user_tg_id
    message = (
        f'Enter new name for user "{user_name}"\n\n'
        "Please use this format:\n"
        "FirstName LastName\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return USER_RENAME_DIALOG


async def rename_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        first_name, last_name = update.message.text.split(" ")
    except ValueError:
        pass  # TODO: catch error
    alterbar_db.renameUserByID(
        context.user_data["edit_user_user_id"], first_name, last_name
    )
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def delete_user_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_tg_id = int(query.data.split("delete_")[1])
    user = alterbar_db.getUserByID(user_tg_id)
    user_name = user.first_name + " " + user.last_name
    keyboard = [
        [
            InlineKeyboardButton(
                "Yes, i'm sure", callback_data="deleteconfirmed_" + str(user_tg_id)
            )
        ],
        [InlineKeyboardButton("No, never", callback_data="cancel")],
        [InlineKeyboardButton("Back", callback_data="user_" + str(user_tg_id))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Deleting user "{user_name}"\nAre you sure?', reply_markup=reply_markup
    )
    return USER_DELETE_DIALOG


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_tg_id = int(query.data.split("deleteconfirmed_")[1])
    alterbar_db.deleteUserByID(user_tg_id)
    await query.edit_message_text(text="Done!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if not checkUserID(update.message.from_user.id):
            return None
        await update.message.reply_text("Operation abored!")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Done!")
    return ConversationHandler.END


def returnHandler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Edit users$"), start)],
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
                CallbackQueryHandler(rename_user_dialog, pattern="^rename_"),
                CallbackQueryHandler(edit_user, pattern="^admintoggle_"),
                CallbackQueryHandler(delete_user_dialog, pattern="^delete_"),
                CallbackQueryHandler(user_list_to_edit, pattern="^back$"),
            ],
            USER_RENAME_DIALOG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, rename_user)
            ],
            USER_DELETE_DIALOG: [
                CallbackQueryHandler(delete_user, pattern="^deleteconfirmed_"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(edit_user, pattern="^user_"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
