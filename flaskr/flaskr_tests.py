import os
import unittest
import tempfile
from flaskr import flaskr


class FlaskrTestCase(unittest.TestCase):
    def setup(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def teardown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    # def test_empty_db(self):
    #     rv = self.app.get('/')
    #     assert b'No entries here so far' in rv.data


if __name__ == '__main__':
    unittest.main()
