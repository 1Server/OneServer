#!/usr/bin/env python
import unittest
import test.all_tests
import sys,os

sys.path.insert(0, os.path.dirname(__file__)+"/oneserver")
testSuite = test.all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)
