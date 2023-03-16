import time
from alterbar_tg_menu import *
from alterbar_tg_scene_manager import Scene


def onEnter(msg):
    menu = Menu("Menu header", add_back_button=True)
    submenu = Menu("Menu header2", back_menu=menu, add_back_button=True)
    menu.addButton("One")
    menu.addButton("Two")
    submenu.addButton("Test")
    submenu.addButton("Fest")
    submenu.addButton("Suck")
    menu.show(msg)


def onEvent(event):
    pass


def onExit():
    pass


scene = Scene(onEnter, onEvent, onExit)
