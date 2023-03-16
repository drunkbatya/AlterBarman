import alterbar_tg
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


class Menu:
    def __init__(
        self,
        header: str,
        add_back_button: bool = True,
    ):
        self.header = header
        self.kbd = InlineKeyboardMarkup()
        self.buttons = []
        self.add_back_button = add_back_button

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
        alterbar_tg.bot.answer_callback_query(query.id)
        alterbar_tg.scene_manager.sendEventToScene(callback_btn_number, query.message)

    def show(self, msg):
        alterbar_tg.setTelegramInlineCallback(self.inlineParse)
        self.__addButtons()
        alterbar_tg.bot.send_message(
            msg.from_user.id, self.header, reply_markup=self.kbd
        )

    def back(self, msg):
        alterbar_tg.bot.delete_message(msg.chat.id, msg.message_id)
