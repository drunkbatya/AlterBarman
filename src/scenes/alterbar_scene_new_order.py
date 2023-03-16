import time
from alterbar_tg_menu import *
from alterbar_tg_scene_manager import Scene


class addScene(Scene):
    def onEnter(self, msg):
        self.menu = Menu("Menu header")
        self.menu.addButton("One")
        self.menu.addButton("Two")
        self.menu.show(msg)

    def onEvent(self, event, msg):
        print(f"Event recived {event}")

    def onExit(self, msg):
        self.menu.back(msg)


scene = addScene("new_order")
