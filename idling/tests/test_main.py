 # -*- coding: utf-8 -*-
 #!/bin/env python

import unittest
import os

if __name__ == '__main__':
    ts = unittest.TestSuite()
    loader = unittest.TestLoader()
    ts.addTests(loader.discover(os.getcwd()))
    run = unittest.TextTestRunner()
    run.run(ts)
