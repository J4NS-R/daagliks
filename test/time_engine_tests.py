import sys

sys.path.insert(0, '../src')

import unittest
from time_engine import TimeEngine


class TestTimeEngine(unittest.TestCase):

    def test_something(self):
        engine = TimeEngine(None)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
