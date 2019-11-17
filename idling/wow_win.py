 # -*- coding: utf-8 -*-
 #!/bin/env python
import os
import time
import psutil
import win32gui
import win32con
import win32process
import pyautogui

class WowWin(object):
    def __get_hwnd_by_pid_match(self, hwnd, extra):
        # print(str(extra[0]) + "  " + str(win32process.GetWindowThreadProcessId(hwnd)[1]))
        if win32process.GetWindowThreadProcessId(hwnd)[1] != extra[0]:
            return
        extra.append(hwnd)

    def __get_hwnd_by_pid(self, pid, match):
        extra = [pid, ]
        win32gui.EnumWindows(self.__get_hwnd_by_pid_match, extra)
        if len(extra) < 2:
            return -1
        for x in extra[1:]:
            if match in win32gui.GetWindowText(x):
                return x
        return -1

    def get_hwnd_by_pid(self, pid):
        self.hwnd = self.__get_hwnd_by_pid(pid, self.name)
        return

    def get_phwnd_by_pid(self, pid):
        self.phwnd = self.__get_hwnd_by_pid(pid, self.pname)
        return

    def __set_foreground(self, hwnd):
        if win32gui.GetForegroundWindow() == hwnd:
            return
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        time.sleep(0.5)
        # win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        return

    def __set_minimize(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def foreground(self):
        try:
            self.__set_foreground(self.hwnd)
        except:
            print("foreground failed")
            return False
        return True

    def pforeground(self):
        try:
            self.__set_foreground(self.phwnd)
        except:
            print("pforeground failed")
            return False
        return True

    def minimize(self):
        try:
            self.__set_minimize(self.hwnd)
        except:
            print("minimize failed")
            return False
        return True

    def pminimize(self):
        try:
            self.__set_minimize(self.phwnd)
        except:
            print("pminimize failed")
            return False
        return True

    def isdead(self):
        return not self.process.is_running()

    def reopen(self):
        if not self.isdead():
            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
            while not self.isdead():
                time.sleep(1)
                continue
        self.pforeground()
        pyautogui.press('enter')
        time.sleep(3)
        self.pminimize()
        time.sleep(8)
        find_wow = False
        for i in self.pprocess.children():
            # print(i.name())
            if 'Wow.exe' in i.name():
                find_wow = True
                break

        if find_wow is False:
            return

        self.process = i
        self.pid = self.process.pid
        self.get_hwnd_by_pid(self.pid)
        return

    def __init__(self, hwnd, name, pname):
        self.hwnd = hwnd
        self.name = name
        self.pname = pname
        self.process = psutil.Process(win32process.GetWindowThreadProcessId(hwnd)[1])
        self.pid = self.process.pid
        self.pprocess = self.process.parent()
        self.ppid = self.process.ppid()
        self.get_phwnd_by_pid(self.ppid)
        print("pid ", self.pid, self.ppid)

def __wow_wins_init(hwnd, extra):
    if extra[0] not in win32gui.GetWindowText(hwnd):
        return
    extra.append(WowWin(hwnd, extra[0], extra[1]))

def wow_wins_init(name, pname):
    rc = [name, pname]
    win32gui.EnumWindows(__wow_wins_init, rc)
    return rc[2:]

# def cb_win(hwnd, extra):
#     if 'Notepad' not in win32gui.GetWindowText(hwnd):
#         return
#     wow_win = WowWin(hwnd)
#     wow_win.foreground()
#     time.sleep(2)
#     wow_win.minimize()
#     time.sleep(2)
#     wow_win.pforeground()
#     time.sleep(2)
#     wow_win.minimize()
#     wow_win.reopen()
#     return

# def win32_test():
#     win32gui.EnumWindows(cb_win, None)
#     return

# if __name__ == '__main__':
    # win32_test()

# def test():
#     time.sleep(3)
#     return win32gui.GetForegroundWindow()


# def __test(hwnd, extra):
#     print(hwnd, win32gui.GetWindowText(hwnd), win32process.GetWindowThreadProcessId(hwnd))
