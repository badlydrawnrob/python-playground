'''
Full test fixture example | pg.41

'''

import unittest


def setUpModule():
    'called once, before anything else in this module'
    print(
        'in module {} - setupModule() '.format(__name__)
    )


def tearDownModule():
    'called once, after everything else in this module'
    print(
        'in module {} - tearDownModule() '.format(__name__)
    )


class TestFixtures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        'called once, before any tests'
        print(
            'in class {} - setUpClass() '.format(cls.__name__)
        )

    @classmethod
    def tearDownClass(cls):
        'called once, after all tests, if setUpClass successful'
        print(
            'in class {} tearDownClass() '.format(cls.__name__)
        )

    def setUp(self):
        'called multiple times, before every test method'
        print('in setUp()')

    def tearDown(self):
        'called multiple times, after every test method'
        print('in tearDown()')

    def test_1(self):
        'a test'
        print('in test_1()')

    def test_2(self):
        'another test'
        print('in test_2()')


class TestAddCleanup(TestFixtures):

    def setUp(self):
        TestFixtures.setUp(self)

        # --- add a cleanup method fixture for all tests
        def cleanup_a():
            print('in cleanup_a()')
        self.addCleanup(cleanup_a)

        def test_3(self):
            # --- add a cleanup method fixture for just this test
            def cleanup_b():
                print('in cleanup_b()')
            self.addCleanup(cleanup_b)
            print('in test_3()')
