import unittest

from prime import is_prime

class Tests(unittest.TestCase):
    def test1(self):
        self.assertFalse(is_prime(1))


class Tests(unittest.TestCase):
    def test2(self):
        self.assertFalse(is_prime(2))

if __name__=="__main__":
    unittest.main()