import time
from alterbar_tg_menu import *


def showSceneNewOrder(msg):
    menu = Menu("Menu header", True)
    submenu = Menu("Menu header2", False, menu)
    menu.addButton("One")
    menu.addButton("Two")
    menu.addButton("Back")
    submenu.addButton("Test")
    submenu.addButton("Fest")
    submenu.addButton("Suck")
    menu.show(msg)
    # time.sleep(3)
    # submenu.show(menu.getMainMessage())
    # time.sleep(3)
    # submenu.back(menu.getMainMessage())
    # time.sleep(3)
    # menu.back(msg)
