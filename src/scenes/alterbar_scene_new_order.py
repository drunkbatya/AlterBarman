import time
from alterbar_tg_menu import *


def showSceneNewOrder(msg):
    menu = Menu("Menu header", add_back_button=True)
    submenu = Menu("Menu header2", back_menu=menu, add_back_button=True)
    menu.addButton("One")
    menu.addButton("Two")
    submenu.addButton("Test")
    submenu.addButton("Fest")
    submenu.addButton("Suck")
    menu.show(msg)
