import time
from alterbar_tg_menu import Menu
from alterbar_tg_scene_manager import Scene


class addScene(Scene):
    def onEnter(self, userID):
        self.menu = Menu("Menu header")
        self.menu.addButton("Do it again")
        self.menu.addButton("Nexxxtt scene")
        self.menu.addButton("Do nothing")
        self.menu.show(userID)

    def onEvent(self, event, userID, messageID, scene_manager):
        print(f"Event recived {event}")
        if event == "0":
            scene_manager.nextScene("new_order", userID, messageID)
        if event == "1":
            scene_manager.nextScene("test", userID, messageID)

    def onExit(self, userID, messageID):
        self.menu.back(userID, messageID)


scene = addScene("new_order")
