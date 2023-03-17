import time
from alterbar_tg_menu import *
from alterbar_tg_scene_manager import Scene


class addScene(Scene):
    def onEnter(self, msg):
        self.menu = Menu("Another menu header")
        self.menu.addButton("Do nothing")
        self.menu.show(msg)

    def onEvent(self, event, msg, scene_manager):
        print(f"Event recived {event}")

    def onExit(self, msg):
        self.menu.back(msg)


scene = addScene("test")
