import unittest
from manager import OneServerManager
class TestManager(unittest.TestCase):
    
    def test_Singleton(self):
        first = OneServerManager()
        second = OneServerManager()
        self.assertTrue(first is second, "Not a singleton")