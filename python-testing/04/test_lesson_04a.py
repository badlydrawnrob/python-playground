'''
Introducing pytest | pg.114
===========================
Testing with unittest

'''

import unittest
from unnecessary_math import multiply


class TestUM(unittest.TestCase):

    def test_numbers_3_4(self):
        self.assertEqual(
            multiply(3, 4), 12
        )


if __name__ == '__main__':
    unittest.main()
