import time
from alterbar_tg_menu import Menu
from alterbar_tg_scene_manager import Scene


class addScene(Scene):
    def onEnter(self, userID):
        self.menu = Menu("Another menu header")
        self.menu.addButton("Do nothing")
        self.menu.show(userID)

    def onEvent(self, event, userID, messageID, scene_manager):
        print(f"Event recived {event}")

    def onExit(self, userID, messageID):
        self.menu.back(userID, messageID)


scene = addScene("test")
