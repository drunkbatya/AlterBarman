import alterbar_tg
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


class Menu:
    def __init__(self, header: str, is_main: bool, back_menu: bool = None):
        self.header = header
        self.kbd = InlineKeyboardMarkup()
        self.init_message_id = 0
        self.main_message = None
        self.buttons = []
        self.back_menu = back_menu
        self.is_main = is_main

    def __constructButtonName(self, button_number):
        return str(id(self)) + "_" + str(button_number)

    def __addButtons(self):
        for cur in self.buttons:
            self.kbd.add(cur)

    def getMainMessage(self):
        return self.main_message

    def addButton(self, name: str):
        button_number = len(self.buttons)  # last
        callback_data = self.__constructButtonName(button_number)
        self.buttons.append(
            InlineKeyboardButton(text=name, callback_data=callback_data)
        )

    def inlineParse(self, query):
        callback_data_parsed = query.data.split("_")
        callback_btn_menu_id = callback_data_parsed[0]
        callback_btn_number = callback_data_parsed[1]
        if callback_btn_menu_id != str(id(self)):
            return
        if callback_btn_number == "2":
            return self.back(query.message)
        alterbar_tg.bot.answer_callback_query(query.id)
        print(f"Pressed button {callback_btn_number}")

    def show(self, msg):
        self.__addButtons()
        alterbar_tg.setTelegramInlineCallback(self.inlineParse)
        if self.is_main:
            self.init_message_id = msg.message_id
            self.main_message = alterbar_tg.bot.send_message(
                msg.from_user.id, self.header, reply_markup=self.kbd
            )
        else:
            alterbar_tg.bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=self.header,
                reply_markup=self.kbd,
            )

    def back(self, msg):
        if self.back_menu is None:
            alterbar_tg.bot.delete_message(msg.from_user.id, self.init_message_id)
            alterbar_tg.bot.delete_message(msg.from_user.id, msg.message_id)
        else:
            self.back_menu.show(msg)
