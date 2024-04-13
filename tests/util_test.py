import unittest
from geometry_dash_recreation import util

class UtilTest(unittest.TestCase):
    def test_csv_reader(self):
        self.assertEqual(util.csv_reader("tests/csv_test.csv"),
                         (("Hello", "World"),
                          ("foo", "bar"),
                          ("amogus", "is", "sus"),
                          (69.0, 420.0, 1337.0),
                          58008.0,
                          ""))

if __name__ == "__main__":
    unittest.main()
