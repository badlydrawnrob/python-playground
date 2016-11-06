'''
Example setUp(), tearDown() | pg. 37

'''

import unittest


class TestLists(unittest.TestCase):

    def setUp(self):
        print('')
        print('in {} - setUp()'.format(self.id()))
        self.myList = [1, 2, 3, 4]

    def test_len(self):
        print('in {} - test_len()'.format(self.id()))
        self.assertEqual(
            len(self.myList), 4
        )

    def test_min(self):
        print('in {} test_min()'.format(self.id()))
        self.assertEqual(min(self.myList), 1)

    def tearDown(self):
        print('in {} - tearDown()'.format(self.id()))
