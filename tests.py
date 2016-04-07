import unittest
import tempfile
import os

from flask import g, url_for

#Import helpers
from app import app
from app.db import DB

#Import models
import app.readings.models as readings_model
import app.content.models as content_model


class FlaskTestCase(unittest.TestCase):
    # This is a helper class that sets up the proper Flask execution context
    # so that the test cases that inherit it will work properly.
    def setUp(self):
        # Allow exceptions (if any) to propagate to the test client.
        app.testing = True

        # Create a test client.
        self.client = app.test_client(use_cookies=True)

        # Create an application context for testing.
        self.app_context = app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        # Clean up the application context.
        self.app_context.pop()

class ApplicationTestCase(FlaskTestCase):
    """Test the basic behavior of page routing and display"""

    def test_home_page(self):
        """Verify the home page."""
        resp = self.client.get('/')
        self.assertTrue('Welcome to the Center for Scripture Engagement' in str(resp.data), "Didn't find welcome message on home page")

    def test_reading_index(self):
        """Verify the reading index page."""
        resp = self.client.get(url_for('readings.all_readings'))
        self.assertTrue('All Readings' in str(resp.data))


#Base class for testing models
class ModelTestCase(FlaskTestCase):
    """Test database access and update functions."""

    # This method is invoked once before all the tests in this test case.
    @classmethod
    def setUpClass(cls):
        """So that we don't overwrite application data, create a temporary database file."""
        (file_descriptor, cls.file_name) = tempfile.mkstemp()
        os.close(file_descriptor)

    # This method is invoked once after all the tests in this test case.
    @classmethod
    def tearDownClass(cls):
        """Remove the temporary database file."""
        os.unlink(cls.file_name)

    def setUp(self):
        """Open the database connection and create all the tables."""
        super(ModelTestCase, self).setUp()
        g.db = DB(db_path = self.file_name)
        g.db.executeScript('app/db/create-db.sql')

    def tearDown(self):
        """Clear all tables in the database and close the connection."""
        g.db.executeScript('app/db/clear-db.sql')
        g.db.close(False)
        super(ModelTestCase, self).tearDown()

class ReadingsTestCase(ModelTestCase):

    example_reading = {
        "name": "Some reading",
        "description": "A description",
        "passage": "John 3:16"
    }

    def test_create_reading(self):
        """Check that readings can be created"""
        row_count = readings_model.add_reading_to_db(self.example_reading["name"], self.example_reading["description"], self.example_reading["passage"])
        self.assertEqual(row_count, 1)

        #Should have an index of 1
        test_reading = readings_model.find_reading(1)
        self.assertIsNotNone(test_reading, "Only one reading should be inserted into the DB")

        #Make sure the inserted reading matches our test data
        self.assertEqual(test_reading["name"], self.example_reading["name"])
        self.assertEqual(test_reading["text"], self.example_reading["description"])
        self.assertEqual(test_reading["BG_passage_reference"], self.example_reading["passage"])

    def test_update_reading(self):
        """Ensure that readings can be updated"""
        row_count = readings_model.add_reading_to_db(self.example_reading["name"], self.example_reading["description"], self.example_reading["passage"])
        self.assertEqual(row_count, 1)

        #Check if the update was actually executed in the DB
        row_count = readings_model.update_reading(1, "Updated reading", "Some words in the description", "Genesis 1:1")
        self.assertEqual(row_count, 1, "One reading row should be updated")

        #Grab the created reading from the database and make sure its data matches the updated data
        test_reading = readings_model.find_reading(1)
        self.assertIsNotNone(test_reading)
        self.assertEqual(test_reading["name"], "Updated reading")
        self.assertEqual(test_reading["text"], "Some words in the description")
        self.assertEqual(test_reading["BG_passage_reference"], "Genesis 1:1")




if __name__ == '__main__':
    unittest.main()
