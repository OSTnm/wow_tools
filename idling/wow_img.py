 # -*- coding: utf-8 -*-
 #!/bin/env python
import cv2
import numpy as np
# import matplotlib.pyplot as plt
from PIL import ImageGrab
from PIL import Image
# from skimage.measure import compare_ssim
import win32gui

IMG_PREFIX        = 'classic/'
IMG_ENTRY_NAME    = IMG_PREFIX + 'entry.jpeg'
IMG_QUEUE_NAME    = IMG_PREFIX + 'queue.jpeg'
IMG_OFFLINE_NAME  = IMG_PREFIX + 'offline.jpeg'
IMG_OFFLINE2_NAME = IMG_PREFIX + 'offline2.jpeg'

IMG_SELECTION_ENTRY    = [0.465, 0.900, 0.070, 0.030]
IMG_SELECTION_QUEUE    = [0.470, 0.541, 0.060, 0.020]
IMG_SELECTION_OFFLINE  = [0.405, 0.460, 0.192, 0.080]
IMG_SELECTION_OFFLINE2 = [0.480, 0.490, 0.050, 0.062]

IMG_ENTRY = Image.open(IMG_ENTRY_NAME, "r")
IMG_QUEUE = Image.open(IMG_QUEUE_NAME, "r")
IMG_OFFLINE = Image.open(IMG_OFFLINE_NAME, "r")
IMG_OFFLINE2 = Image.open(IMG_OFFLINE2_NAME, "r")

IMG_CUT_OFF = 5
IMG_DIFF_HIST = 0.80

def img_histogram_get(img):
    H = cv2.calcHist([img], [1], None, [256], [0, 256])
    H = cv2.normalize(H, H, 0, 1, cv2.NORM_MINMAX, -1)
    return H

def img_get_diff_hist(img1, img2):
    H1 = img_histogram_get(img1)
    H2 = img_histogram_get(img2)
    # plt.subplot(2, 1, 1)
    # plt.plot(H1,label="img1")
    # plt.plot(H2,label="img2")
    # plt.legend()
    # plt.show()
    rc = cv2.compareHist(H1, H2, 0)
    print(rc)
    return rc

def img_get_diff(img1, img2):
    x, y = img2.size

    # img1 = np.array(img1.resize((x, y)))
    # img2 = np.array(img2.resize((x, y)))

    img1 = np.array(img1)
    img2 = np.array(img2)

    try:
        img1 = np.resize(img1, (img2.shape[0], img2.shape[1], img2.shape[2]))
    except Exception as e:
        print("numpy resize failed, skip it")
        return 0

    return img_get_diff_hist(img1, img2)
    # return compare_ssim(img1, img2, multichannel=True)

def grab(hwnd, selection, show, save, name):
    [w_tl_x, w_tl_y, w_br_x, w_br_y] = win32gui.GetWindowRect(hwnd)
    w_size_x = w_br_x - w_tl_x
    w_size_y = w_br_y - w_tl_y
    tl_x = w_tl_x + int(w_size_x * selection[0])
    tl_y = w_tl_y + int(w_size_y * selection[1])
    br_x =   tl_x + int(w_size_x * selection[2])
    br_y =   tl_y + int(w_size_y * selection[3])
    img = ImageGrab.grab([tl_x, tl_y, br_x, br_y])
    if show:
        img.show()
    if save:
        img.save(name, quality=100)
    return [img, [tl_x, tl_y]]

def grab_entry(hwnd):
    return grab(hwnd, IMG_SELECTION_ENTRY, False, False, IMG_ENTRY_NAME)

def grab_queue(hwnd):
    return grab(hwnd, IMG_SELECTION_QUEUE, False, False, IMG_QUEUE_NAME)

def grab_offline(hwnd):
    return grab(hwnd, IMG_SELECTION_OFFLINE, False, False, IMG_OFFLINE_NAME)

def grab_offline2(hwnd):
    return grab(hwnd, IMG_SELECTION_OFFLINE2, False, False, IMG_OFFLINE2_NAME)

def img_dhash(img):
    rc = []

    if img.shape[1] < 1:
        return 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1] - 1):
            rc.append(1 if img[i, j] > img[i, j + 1] else 0)
    # print(rc)
    return rc

def img_hamming_distance(hash1, hash2):
    num = 0

    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            num += 1

    # print(num)
    return num

def img_get_diff_hamming(img1, img2):
    dist = img_hamming_distance(img_dhash(img1), img_dhash(img2))
    sim = 1 - dist * 1.0 / (x * y)
    return sim
