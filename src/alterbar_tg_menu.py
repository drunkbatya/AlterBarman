import alterbar_tg
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


class Menu:
    def __init__(
        self,
        header: str,
        back_menu: bool = None,
        add_back_button: bool = True,
    ):
        self.header = header
        self.kbd = InlineKeyboardMarkup()
        self.buttons = []
        self.back_menu = back_menu
        self.add_back_button = add_back_button
        self.first_show = True
        self.init_message_id = 0

    def __constructButtonName(self, button_number):
        return str(id(self)) + "_" + str(button_number)

    def __addButtons(self):
        for cur in self.buttons:
            self.kbd.add(cur)
        if self.add_back_button:
            self.kbd.add(
                InlineKeyboardButton(
                    text="Back", callback_data=self.__constructButtonName("back")
                )
            )

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
        if callback_btn_number == "back":
            return self.back(query.message)
        alterbar_tg.bot.answer_callback_query(query.id)
        alterbar_tg.scene_manager.sendEventToScene(callback_btn_number)
        print(f"Pressed button {callback_btn_number}")

    def show(self, msg):
        alterbar_tg.setTelegramInlineCallback(self.inlineParse)
        if self.first_show:
            self.__addButtons()
            self.first_show = False
            if self.back_menu is None:
                self.init_message_id = msg.message_id
                return alterbar_tg.bot.send_message(
                    msg.from_user.id, self.header, reply_markup=self.kbd
                )
        alterbar_tg.bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            text=self.header,
            reply_markup=self.kbd,
        )

    def back(self, msg):
        if self.back_menu is None:
            alterbar_tg.bot.delete_message(msg.chat.id, msg.message_id)
            alterbar_tg.bot.delete_message(msg.chat.id, self.init_message_id)
        else:
            self.back_menu.show(msg)
