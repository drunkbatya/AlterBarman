#!/usr/bin/env python3
import atexit
from lib.tg import startTelegramBot
from lib.db import databaseInit, databaseCloseSession


def atExit():
    databaseCloseSession()


if __name__ == "__main__":
    atexit.register(atExit)
    databaseInit()
    startTelegramBot()
