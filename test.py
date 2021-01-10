import unittest
from src import python


class MyTestCase(unittest.TestCase):
	def test_something(self):
		self.assertEqual(True, True)


if __name__ == '__main__':
	unittest.main()
