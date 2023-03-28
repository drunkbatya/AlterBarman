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

(
    EDIT_START,
    EDIT_PRODUCTS_SELECT_CATEGORY,
    EDIT_OR_ADD_UNITS,
    UNITS_LIST_TO_EDIT,
    EDIT_UNITS,
    EDIT_UNITS_ASK_SHORT_NAME_FOR_CHANGE,
    EDIT_UNITS_ASK_FULL_NAME_FOR_CHANGE,
    ADD_UNITS_ASK_SHORT_NAME,
    ADD_UNITS_ASK_FULL_NAME,
    UNIT_DELETE_DIALOG,
    EDIT_OR_ADD_CURRENCIES,
    CURRENCIES_LIST_TO_EDIT,
    EDIT_CURRENCIES,
    EDIT_CURRENCIES_ASK_SHORT_NAME_FOR_CHANGE,
    EDIT_CURRENCIES_ASK_FULL_NAME_FOR_CHANGE,
    ADD_CURRENCIES_ASK_SHORT_NAME,
    ADD_CURRENCIES_ASK_FULL_NAME,
    CURRENCY_DELETE_DIALOG,
    EDIT_OR_ADD_CATEGORIES,
    CATEGORIES_LIST_TO_EDIT,
    EDIT_CATEGORIES,
    EDIT_CATEGORIES_ASK_SHORT_NAME_FOR_CHANGE,
    EDIT_CATEGORIES_ASK_FULL_NAME_FOR_CHANGE,
    ADD_CATEGORIES_ASK_SHORT_NAME,
    ADD_CATEGORIES_ASK_FULL_NAME,
    CATEGORIES_DELETE_DIALOG,
) = range(26)


def constructCategoriesInlineKeybord(categories) -> InlineKeyboardMarkup:
    buttons = []
    for current in categories:
        button_name = current.name
        callback_data = "category_" + str(current.id)
        buttons.append([InlineKeyboardButton(button_name, callback_data=callback_data)])
    buttons.append([InlineKeyboardButton("Back", callback_data="back")])
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Edit products", callback_data="edit_products")],
        [InlineKeyboardButton("Edit units", callback_data="edit_units")],
        [InlineKeyboardButton("Edit currencies", callback_data="edit_currencies")],
        [InlineKeyboardButton("Edit categories", callback_data="edit_categories")],
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
    return EDIT_START


# Products
async def edit_products_select_category(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    categories = alterbar_db.getAllCategories()
    reply_markup = constructCategoriesInlineKeybord(categories)
    if len(categories):
        msg = "Select product category"
    else:
        msg = "No product categories found!\n\nYou need to add one from previous menu."
    await query.edit_message_text(text=msg, reply_markup=reply_markup)
    return EDIT_PRODUCTS_SELECT_CATEGORY


# Units
def constructUnitsInlineKeybord(units) -> InlineKeyboardMarkup:
    buttons = []
    for current in units:
        button_name = f"{current.name_full} ({current.name_short})"
        callback_data = "unit_" + str(current.id)
        buttons.append([InlineKeyboardButton(button_name, callback_data=callback_data)])
    buttons.append([InlineKeyboardButton("Back", callback_data="back")])
    return InlineKeyboardMarkup(buttons)


async def edit_or_add_units(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Add unit", callback_data="add_unit")],
        [InlineKeyboardButton("Edit unit", callback_data="edit_unit")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="What do you want to do?", reply_markup=reply_markup
    )
    return EDIT_OR_ADD_UNITS


async def add_units_ask_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["add_units_short_name"] = update.message.text
    message = (
        "Enter full name for new unit\n\n"
        "Example: millilitre\n\n"
        "Send /cancel to abort this operation"
    )
    await update.message.reply_text(text=message)
    return ADD_UNITS_ASK_FULL_NAME


async def add_units_ask_short_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    message = (
        "Enter short name for new unit\n\n"
        "Example: ml\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return ADD_UNITS_ASK_SHORT_NAME


async def add_unit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    short_name = context.user_data["add_units_short_name"]
    full_name = update.message.text
    alterbar_db.addUnit(short_name, full_name)
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def units_list_to_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    units = alterbar_db.getAllUnits()
    reply_markup = constructUnitsInlineKeybord(units)
    if len(units):
        msg = "Select unit to edit"
    else:
        msg = "No units found!\n\nYou need to add one from previous menu."
    await query.edit_message_text(text=msg, reply_markup=reply_markup)
    return UNITS_LIST_TO_EDIT


async def edit_unit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    unit_id = query.data.split("unit_")[1]
    unit = alterbar_db.getUnitByID(int(unit_id))
    keyboard = [
        [
            InlineKeyboardButton(
                "Change short name", callback_data="change_short_name_" + unit_id
            )
        ],
        [
            InlineKeyboardButton(
                "Change full name", callback_data="change_full_name_" + unit_id
            )
        ],
        [InlineKeyboardButton("Delete", callback_data="delete_" + unit_id)],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Edit unit "{unit.name_full} ({unit.name_short})"',
        reply_markup=reply_markup,
    )
    return EDIT_UNITS


async def edit_units_ask_short_name_for_change(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    unit_id = query.data.split("change_short_name_")[1]
    context.user_data["edit_units_change_short_name_unit_id"] = unit_id
    unit = alterbar_db.getUnitByID(int(unit_id))
    message = (
        f"Enter new short name for unit {unit.name_full}\n\n"
        f"Current value: {unit.name_short}\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return EDIT_UNITS_ASK_SHORT_NAME_FOR_CHANGE


async def edit_units_change_short_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    unit_id = context.user_data["edit_units_change_short_name_unit_id"]
    short_name = update.message.text
    alterbar_db.changeUnitShortNameByID(unit_id, short_name)
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def edit_units_ask_full_name_for_change(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    unit_id = query.data.split("change_full_name_")[1]
    context.user_data["edit_units_change_full_name_unit_id"] = unit_id
    unit = alterbar_db.getUnitByID(int(unit_id))
    message = (
        f"Enter new full name for unit {unit.name_full}\n\n"
        f"Current value: {unit.name_full}\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return EDIT_UNITS_ASK_FULL_NAME_FOR_CHANGE


async def edit_units_change_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    unit_id = context.user_data["edit_units_change_full_name_unit_id"]
    full_name = update.message.text
    alterbar_db.changeUnitFullNameByID(unit_id, full_name)
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def delete_unit_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    unit_id = query.data.split("delete_")[1]
    unit = alterbar_db.getUnitByID(int(unit_id))
    keyboard = [
        [
            InlineKeyboardButton(
                "Yes, i'm sure", callback_data="deleteconfirmed_" + unit_id
            )
        ],
        [InlineKeyboardButton("No, never", callback_data="cancel")],
        [InlineKeyboardButton("Back", callback_data="unit_" + unit_id)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Deleting unit "{unit.name_full} ({unit.name_short})"\nAre you sure?',
        reply_markup=reply_markup,
    )
    return UNIT_DELETE_DIALOG


async def delete_unit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    unit_id = query.data.split("deleteconfirmed_")[1]
    alterbar_db.deleteUnitByID(unit_id)
    await query.edit_message_text(text="Done!")
    return ConversationHandler.END


# Currencies
def constructCurrenciesInlineKeybord(currencies) -> InlineKeyboardMarkup:
    buttons = []
    for current in currencies:
        button_name = f"{current.name_full} ({current.name_short})"
        callback_data = "currency_" + str(current.id)
        buttons.append([InlineKeyboardButton(button_name, callback_data=callback_data)])
    buttons.append([InlineKeyboardButton("Back", callback_data="back")])
    return InlineKeyboardMarkup(buttons)


async def edit_or_add_currencies(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Add currency", callback_data="add_currency")],
        [InlineKeyboardButton("Edit currency", callback_data="edit_currency")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="What do you want to do?", reply_markup=reply_markup
    )
    return EDIT_OR_ADD_CURRENCIES


async def add_currencies_ask_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["add_currencies_short_name"] = update.message.text
    message = (
        "Enter full name for new currency\n\n"
        "Example: United States dollar\n\n"
        "Send /cancel to abort this operation"
    )
    await update.message.reply_text(text=message)
    return ADD_CURRENCIES_ASK_FULL_NAME


async def add_currencies_ask_short_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    message = (
        "Enter short name for new currency\n\n"
        "Example: USD\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return ADD_CURRENCIES_ASK_SHORT_NAME


async def add_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    short_name = context.user_data["add_currencies_short_name"]
    full_name = update.message.text
    alterbar_db.addCurrency(short_name, full_name)
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def currencies_list_to_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    currencies = alterbar_db.getAllCurrencies()
    reply_markup = constructCurrenciesInlineKeybord(currencies)
    if len(currencies):
        msg = "Select currency to edit"
    else:
        msg = "No currencies found!\n\nYou need to add one from previous menu."
    await query.edit_message_text(text=msg, reply_markup=reply_markup)
    return CURRENCIES_LIST_TO_EDIT


async def edit_currencies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    currency_id = query.data.split("currency_")[1]
    currency = alterbar_db.getCurrencyByID(int(currency_id))
    keyboard = [
        [
            InlineKeyboardButton(
                "Change short name", callback_data="change_short_name_" + currency_id
            )
        ],
        [
            InlineKeyboardButton(
                "Change full name", callback_data="change_full_name_" + currency_id
            )
        ],
        [InlineKeyboardButton("Delete", callback_data="delete_" + currency_id)],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Edit currency "{currency.name_full} ({currency.name_short})"',
        reply_markup=reply_markup,
    )
    return EDIT_CURRENCIES


async def edit_currencies_ask_short_name_for_change(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    currency_id = query.data.split("change_short_name_")[1]
    context.user_data["edit_currencies_change_short_name_currency_id"] = currency_id
    currency = alterbar_db.getCurrencyByID(int(currency_id))
    message = (
        f"Enter new short name for currency {currency.name_full}\n\n"
        f"Current value: {currency.name_short}\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return EDIT_CURRENCIES_ASK_SHORT_NAME_FOR_CHANGE


async def edit_currencies_change_short_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    currency_id = context.user_data["edit_currencies_change_short_name_currency_id"]
    short_name = update.message.text
    alterbar_db.changeCurrencyShortNameByID(currency_id, short_name)
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def edit_currencies_ask_full_name_for_change(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    currency_id = query.data.split("change_full_name_")[1]
    context.user_data["edit_currencies_change_full_name_currency_id"] = currency_id
    currency = alterbar_db.getCurrencyByID(int(currency_id))
    message = (
        f"Enter new full name for currency {currency.name_full}\n\n"
        f"Current value: {currency.name_full}\n\n"
        "Send /cancel to abort this operation"
    )
    await query.edit_message_text(text=message)
    return EDIT_CURRENCIES_ASK_FULL_NAME_FOR_CHANGE


async def edit_currencies_change_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    currency_id = context.user_data["edit_currencies_change_full_name_currency_id"]
    full_name = update.message.text
    alterbar_db.changeCurrencyFullNameByID(currency_id, full_name)
    await update.message.reply_text(text="Done!")
    return ConversationHandler.END


async def delete_currency_dialog(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    currency_id = query.data.split("delete_")[1]
    currency = alterbar_db.getCurrencyByID(int(currency_id))
    keyboard = [
        [
            InlineKeyboardButton(
                "Yes, i'm sure", callback_data="deleteconfirmed_" + currency_id
            )
        ],
        [InlineKeyboardButton("No, never", callback_data="cancel")],
        [InlineKeyboardButton("Back", callback_data="currency_" + currency_id)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Deleting currency "{currency.name_full} ({currency.name_short})"\nAre you sure?',
        reply_markup=reply_markup,
    )
    return CURRENCY_DELETE_DIALOG


async def delete_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    currency_id = query.data.split("deleteconfirmed_")[1]
    alterbar_db.deleteCurrencyByID(currency_id)
    await query.edit_message_text(text="Done!")
    return ConversationHandler.END


# Categories
async def edit_or_add_categories(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Add category", callback_data="add_category")],
        [InlineKeyboardButton("Edit category", callback_data="edit_category")],
        [InlineKeyboardButton("Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="What do you want to do?", reply_markup=reply_markup
    )
    return EDIT_OR_ADD_CATEGORIES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if not alterbar_db.checkUserID(update.message.from_user.id):
            return None
        await update.message.reply_text("Operation abored!")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Done!")
    return ConversationHandler.END


def returnHandler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Edit menu$"), start)],
        states={
            EDIT_START: [
                CallbackQueryHandler(
                    edit_products_select_category, pattern="^edit_products$"
                ),
                CallbackQueryHandler(edit_or_add_units, pattern="^edit_units$"),
                CallbackQueryHandler(
                    edit_or_add_currencies, pattern="^edit_currencies$"
                ),
                CallbackQueryHandler(
                    edit_or_add_categories, pattern="^edit_categories$"
                ),
                CallbackQueryHandler(cancel, pattern="^back$"),
            ],
            EDIT_PRODUCTS_SELECT_CATEGORY: [
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            EDIT_OR_ADD_UNITS: [
                CallbackQueryHandler(add_units_ask_short_name, pattern="^add_unit$"),
                CallbackQueryHandler(units_list_to_edit, pattern="^edit_unit$"),
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            ADD_UNITS_ASK_SHORT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_units_ask_full_name)
            ],
            ADD_UNITS_ASK_FULL_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_unit)
            ],
            UNITS_LIST_TO_EDIT: [
                CallbackQueryHandler(edit_unit, pattern="^unit_"),
                CallbackQueryHandler(edit_or_add_units, pattern="^back$"),
            ],
            EDIT_UNITS: [
                CallbackQueryHandler(
                    edit_units_ask_short_name_for_change, pattern="^change_short_name_"
                ),
                CallbackQueryHandler(
                    edit_units_ask_full_name_for_change, pattern="^change_full_name_"
                ),
                CallbackQueryHandler(delete_unit_dialog, pattern="^delete_"),
                CallbackQueryHandler(units_list_to_edit, pattern="^back$"),
            ],
            EDIT_UNITS_ASK_SHORT_NAME_FOR_CHANGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, edit_units_change_short_name
                )
            ],
            EDIT_UNITS_ASK_FULL_NAME_FOR_CHANGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, edit_units_change_full_name
                )
            ],
            UNIT_DELETE_DIALOG: [
                CallbackQueryHandler(delete_unit, pattern="^deleteconfirmed_"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(edit_unit, pattern="^unit_"),
            ],
            EDIT_OR_ADD_CURRENCIES: [
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            EDIT_OR_ADD_CURRENCIES: [
                CallbackQueryHandler(
                    add_currencies_ask_short_name, pattern="^add_currency$"
                ),
                CallbackQueryHandler(
                    currencies_list_to_edit, pattern="^edit_currency$"
                ),
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            ADD_CURRENCIES_ASK_SHORT_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, add_currencies_ask_full_name
                )
            ],
            ADD_CURRENCIES_ASK_FULL_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_currency)
            ],
            CURRENCIES_LIST_TO_EDIT: [
                CallbackQueryHandler(edit_currencies, pattern="^currency_"),
                CallbackQueryHandler(edit_or_add_currencies, pattern="^back$"),
            ],
            EDIT_CURRENCIES: [
                CallbackQueryHandler(
                    edit_currencies_ask_short_name_for_change,
                    pattern="^change_short_name_",
                ),
                CallbackQueryHandler(
                    edit_currencies_ask_full_name_for_change,
                    pattern="^change_full_name_",
                ),
                CallbackQueryHandler(delete_currency_dialog, pattern="^delete_"),
                CallbackQueryHandler(currencies_list_to_edit, pattern="^back$"),
            ],
            EDIT_CURRENCIES_ASK_SHORT_NAME_FOR_CHANGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, edit_currencies_change_short_name
                )
            ],
            EDIT_CURRENCIES_ASK_FULL_NAME_FOR_CHANGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, edit_currencies_change_full_name
                )
            ],
            CURRENCY_DELETE_DIALOG: [
                CallbackQueryHandler(delete_currency, pattern="^deleteconfirmed_"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(edit_currencies, pattern="^currency_"),
            ],
            EDIT_OR_ADD_CATEGORIES: [
                CallbackQueryHandler(start, pattern="^back$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
