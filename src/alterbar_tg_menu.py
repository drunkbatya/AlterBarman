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

    def checkInlineButtonLink(self, btnMenuID, queryID) -> bool:
        if btnMenuID != str(id(self)):
            return False
        alterbar_tg.bot.answer_callback_query(queryID)
        return True

    def addButton(self, name: str):
        button_number = len(self.buttons)  # last
        callback_data = self.__constructButtonName(button_number)
        self.buttons.append(
            InlineKeyboardButton(text=name, callback_data=callback_data)
        )

    def show(self, userID):
        self.__addButtons()
        alterbar_tg.bot.send_message(userID, self.header, reply_markup=self.kbd)

    def back(self, userID, messageID):
        alterbar_tg.bot.delete_message(userID, messageID)
