# -*- coding: utf-8 -*-
#!/bin/env python
import webbrowser
import sys
import os
import time
# try:
#     from win10toast import ToastNotifier
#     win10toast_load = True
# except:
#     win10toast_load = False
#     pass
import threading
from infi.systray import SysTrayIcon
from pynput.keyboard import Listener, Key
# error if converting to exe, use win instance directly
from plyer import notification
try:
    import plyer.platforms.win.notification
    notification = plyer.platforms.win.notification.instance()
except:
    notification = None
pass
# notification = None
IDLING_ICO = 'idling.ico'

SYSTRAY = None
RUNNING = False
NOTIFY  = False

app = "WoW Idling by ostnm"
app_title = 'Wow Idling'
app_lock  = threading.Lock()

welcome_msg = "Welcome to use idling, Press 'Home' to active/pause it"
active_msg = "Idling is running"
pause_msg  = "Idling is on pause"

def __app_pause(systray):
    global RUNNING
    RUNNING = not RUNNING
    text = app if RUNNING else app + " - On Pause"
    systray.update(hover_text=text)
    return

def app_pause(systray):
    app_lock.acquire()
    __app_pause(systray)
    app_lock.release()

def app_about(systray):
    return

def app_destroy(systray):
    os._exit(0)

def app_press(key):
    global NOTIFY
    if not key is Key.home:
        return
    if not NOTIFY:
        app_pause(SYSTRAY)
        NOTIFY = True

def app_keybind():
    with Listener(on_press = app_press) as listener:
        listener.join()

def app_notify():
    global NOTIFY
    while True:
        time.sleep(3)
        if NOTIFY:
            msg = active_msg if RUNNING else pause_msg
            if notification:
                notification.notify(title=app_title, message=msg, app_name=app, app_icon=IDLING_ICO, timeout=3)
        NOTIFY = False

def wow_gui_setup():
    global SYSTRAY
    app_ico = IDLING_ICO
    menu_options = (("Start/Stop", None, app_pause), )
    SYSTRAY = SysTrayIcon(app_ico, app,
                          menu_options, on_quit=app_destroy)
    SYSTRAY.start()
    threading.Thread(target=app_keybind).start()
    if notification:
        notification.notify(title=app_title, message=welcome_msg, app_name=app, app_icon=IDLING_ICO, timeout=3)
    threading.Thread(target=app_notify).start()
