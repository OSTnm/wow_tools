 # -*- coding: utf-8 -*-
 #!/bin/env python
import unittest
import sys
sys.path.append(".")
import wow_img
from PIL import Image

class TestWowImg(unittest.TestCase):
    def test_img_get_diff(self):
        img_list = [wow_img.IMG_ENTRY, wow_img.IMG_QUEUE, wow_img.IMG_OFFLINE, wow_img.IMG_OFFLINE2]
        for img1 in img_list:
            for img2 in img_list:
                if img1 is img2:
                    self.assertAlmostEqual(wow_img.img_get_diff(img1, img2), 1.0, delta = 1e-4)
                else:
                    self.assertLess(wow_img.img_get_diff(img1, img2), 0.2)

if __name__ == '__main__':
    unittest.main()
