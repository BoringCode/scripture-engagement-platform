import unittest
import os

from flask import g, url_for

from app import app

#@unittest.skip
class TrivialTestCase(unittest.TestCase):
    # This method is invoked before EVERY test_xxx method.
    def setUp(self):
        print("In setUp method")

    # This method is invoked after EVERY test_xxx method.
    def tearDown(self):
        print("In tearDown method")

    def test_should_pass(self):
        print("In test_should_pass")
        self.assertTrue(1 == 1)

    @unittest.expectedFailure
    def test_should_fail(self):
        print("In test_should_fail")
        self.assertTrue(1 == 2)


if __name__ == '__main__':
    unittest.main()
