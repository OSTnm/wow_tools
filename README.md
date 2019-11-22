# Wow Tools ![wow_tools.python](wow_tools.png)
> **Wow Tools** is a series of tools for world of warcraft, free and simple for me.

[![Build Status](https://travis-ci.com/OSTnm/wow_tools.svg?branch=master)](https://travis-ci.com/OSTnm/wow_tools)

- [Idling](#Idling)

## Idling

Idling keeps game character online and login automatically when being offline.

| Platform                       | World of Warcraft Versoin | Factions | Game Instances | Geometry  | Test Result |
| ------------------------------ | ------------------------- | ---------| -------------- | --------- | ----------- |
| Win10                          | Vanilla, Chinese          | Alliance |              1 | 1920X1080 | ✔ |
| Win10                          | Vanilla, Chinese          | Alliance |              3 | 1920X1080 | ✔ |

### Usage

- python idling.py
- type 'home' to activate/pause it
<img src="idling/wow_idling_running.png" width = 20% height = 20% />
<img src="idling/wow_idling_on_pause.png" width = 20% height = 20% />

- quit
<img src="idling/wow_idling_quit.png" width = 20% height = 20% />

### Exe

**./install.sh**, note that it is based on bash, [git-bash](https://gitforwindows.org/) is recommended.

### How

- prompt character selection screen, login if yes.
- prompt queuing screen, do nothing.
- prompt offline screen, close wow instance and find parent battle.net, boot it again.

### Dependency

- pyautogui
- opencv-python
- psutil
- pywin32
- plyer
- infi.systray
- pillow
- pynput
- tendo
- pyinstaller
- scikit-image

### Limitation

Only track existing wow instances for better performace.


# License

**Wow Tools** is released under the terms of Apache License, Version 2.0. Please refer to the LICENSE file.

- - -

