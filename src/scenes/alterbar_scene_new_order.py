import time
from alterbar_tg_menu import *
from alterbar_tg_scene_manager import Scene


class addScene(Scene):
    def onEnter(self, msg):
        self.menu = Menu("Menu header")
        self.menu.addButton("Do it again")
        self.menu.addButton("Nexxxtt scene")
        self.menu.addButton("Do nothing")
        self.menu.show(msg)

    def onEvent(self, event, msg, scene_manager):
        print(f"Event recived {event}")
        if event == "0":
            scene_manager.nextScene("new_order", msg)
        if event == "1":
            scene_manager.nextScene("test", msg)

    def onExit(self, msg):
        self.menu.back(msg)


scene = addScene("new_order")
