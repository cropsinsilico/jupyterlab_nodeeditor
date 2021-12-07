import unittest
from yggdrasil_support import *

# I will start with just Photosynthesis model testing, then move on to develop and test custom models

class YggModelTester(unittest.TestCase):

# Junk Function Testing to learn PyTest
    def test_decrement(self):
        self.assertEqual(decrement(3), 2)

    def test_increment(self):
        self.assertEqual(increment(3), 4)

        
if __name__ == "__main__":
    unittest.main()
