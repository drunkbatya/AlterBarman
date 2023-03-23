#!/usr/bin/env python3
import atexit
from alterbar_tg import startTelegramBot
from alterbar_db import databaseInit, updateAuthorizedUserIDs, databaseCloseSession


def atExit():
    databaseCloseSession()


if __name__ == "__main__":
    atexit.register(atExit)
    databaseInit()
    updateAuthorizedUserIDs()
    startTelegramBot()
