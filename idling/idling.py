 # -*- coding: utf-8 -*-
 #!/bin/env python
import sys
import os
#export pbr version for pyinstaller tendo
os.environ["PBR_VERSION"] = '5.4.3'
import time
import pyautogui
import cv2
import threading
import wow_win
import wow_img
import wow_gui
from tendo import singleton
from infi.systray import SysTrayIcon

WOW_WIN_NAME = "魔兽世界"
BATTLE_WIN_NAME = "暴雪战网"

def login(entry):
    pyautogui.moveTo(entry[0], entry[1], 0.5)
    pyautogui.click(interval=0.5)
    # temp cursor location
    pyautogui.moveTo(100, 100, 0.5)

def prompt_login(wow):
    img, entry = wow_img.grab_entry(wow.hwnd)
    if wow_img.img_get_diff(wow_img.IMG_ENTRY, img) < wow_img.IMG_DIFF_HIST:
        return False
    login(entry)
    return True

def prompt_queue(wow):
    img, entry = wow_img.grab_queue(wow.hwnd)
    return wow_img.IMG_DIFF_HIST <= wow_img.img_get_diff(wow_img.IMG_QUEUE, img)

def prompt_offline(wow):
    img, entry = wow_img.grab_offline(wow.hwnd)
    return wow_img.IMG_DIFF_HIST <= wow_img.img_get_diff(wow_img.IMG_OFFLINE, img)

def prompt_offline2(wow):
    img, entry = wow_img.grab_offline2(wow.hwnd)
    return wow_img.IMG_DIFF_HIST <= wow_img.img_get_diff(wow_img.IMG_OFFLINE2, img)

def do_idling(wow):
    wow.foreground()
    if prompt_login(wow):
        return
    if prompt_queue(wow):
        return
    if prompt_offline(wow) or prompt_offline2(wow):
        wow.reopen()
        return
    if wow.isdead():
        wow.reopen()
        return

def idling():
    wow_wins = wow_win.wow_wins_init(WOW_WIN_NAME, BATTLE_WIN_NAME)
    while True:
        if wow_gui.RUNNING:
            for wow in wow_wins:
                do_idling(wow)
                time.sleep(2)
        time.sleep(5)

if __name__ == "__main__":
    me = singleton.SingleInstance()
    if not me:
        os._exit(-1)
    wow_gui.wow_gui_setup()
    idling()
