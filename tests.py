import unittest
import tempfile
import os
import time
from unittest.mock import patch

from flask import g, url_for

#Import helpers
from app import app
from app.db import DB

#Import models
import app.readings.models as readings_model
import app.content.models as content_model
import app.posts.models as posts_model
import app.users.models as users_model

class ProxyUser(users_model.User):
    def __init__(self, user_id = 1, password = False, reload_obj = False):
        """Proxy user for testing model functionality that requires a login"""
        self._user_id = user_id

        self._user = {
            "active": True,
            "first_name": "Fake",
            "last_name": "User",
            "id": self._user_id,
            "email_address": "user@example.com",
            "password": "fake",
            "email": "user@example.com"
        }

        # Add to database
        users_model.register(self._user)

        self._is_active = self._user["active"]
        self._is_authenticated = True

    @staticmethod
    def exists(user_id):
        return True

    def get(self):
        pass

    def check_password(self, password):
        return False

    def set_password(self, password):
        return False

class FlaskTestCase(unittest.TestCase):
    # This is a helper class that sets up the proper Flask execution context
    # so that the test cases that inherit it will work properly.
    def setUp(self):
        # Allow exceptions (if any) to propagate to the test client.
        app.testing = True

        # Don't check for cross site request forgery tokens
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['CSRF_ENABLED'] = False

        # Set database file location
        app.config["DATABASE"] = self.file_name

        app.config["BG_API_KEY"] = self.bg_api_key.name

        # Create a test client.
        self.client = app.test_client(use_cookies=True)

        # Create an application context for testing.
        self.app_context = app.test_request_context()
        self.app_context.push()

        g.db = DB()
        g.db.executeScript('app/db/create-db.sql')

    def tearDown(self):
        # Clean up the application context.
        g.db.executeScript('app/db/clear-db.sql')
        g.db.close(False)
        self.app_context.pop()

    def tempFile(self, permissions = "r+"):
        # Generate new temporary file and return a file object
        (file_descriptor, file_name) = tempfile.mkstemp()
        os.close(file_descriptor)
        return open(file_name, permissions)

    # This method is invoked once before all the tests in this test case.
    @classmethod
    def setUpClass(self):
        """So that we don't overwrite application data, create a temporary database file."""
        (file_descriptor, self.file_name) = tempfile.mkstemp()
        os.close(file_descriptor)

        # Create temp api key file
        self.bg_api_key = self.tempFile("r+")
        self.bg_api_key.write('{ "access_token": "" }')
        self.bg_api_key.flush()

    # This method is invoked once after all the tests in this test case.
    @classmethod
    def tearDownClass(cls):
        """Remove the temporary database file."""
        os.unlink(cls.file_name)
        os.unlink(cls.bg_api_key.name)

    @patch("app.before")
    def before_request():
        # Our setup function already handled the before request functions
        initNav()

    @patch("app.after")
    def after_request(exception):
        pass


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


class ReadingsTestCase(FlaskTestCase):

    example_reading = {
        "name": "Some reading",
        "description": "A description",
        "translation": "NKJV",
        "passage": "Gen 1.1"
    }

    expected_passage = "In the beginning God created the heavens and the earth."

    def setUp(self):
        super(ReadingsTestCase, self).setUp()
        # Use proxy user for these tests
        g.user = ProxyUser()

    def test_create_reading(self):
        """Check that readings can be created"""
        reading_id = readings_model.add_reading_to_db(self.example_reading["name"], self.example_reading["description"], self.example_reading["translation"])
        self.assertTrue(reading_id is not False, "Reading could not be added to database")

        #Should have an index of 1
        test_reading = readings_model.find_reading(reading_id)
        self.assertIsNotNone(test_reading, "Only one reading should be inserted into the DB")

        #Make sure the inserted reading matches our test data
        self.assertEqual(test_reading["name"], self.example_reading["name"])
        self.assertEqual(test_reading["text"], self.example_reading["description"])
        self.assertEqual(test_reading["translation"], self.example_reading["translation"])

    def test_update_reading(self):
        """Ensure that readings can be updated"""
        reading_id = readings_model.add_reading_to_db(self.example_reading["name"], self.example_reading["description"], self.example_reading["translation"])
        self.assertTrue(reading_id is not False, "Reading could not be added to database")

        #Check if the update was actually executed in the DB
        updated = readings_model.update_reading(reading_id, "Updated reading", "Some words in the description", "KJV")
        self.assertTrue(updated is not False, "One reading row should be updated")

        #Grab the created reading from the database and make sure its data matches the updated data
        test_reading = readings_model.find_reading(1)
        self.assertIsNotNone(test_reading)
        self.assertEqual(test_reading["name"], "Updated reading")
        self.assertEqual(test_reading["text"], "Some words in the description")
        self.assertEqual(test_reading["translation"], "KJV")

    @unittest.skip("Invalid BG API key, so don't test for now")
    def test_add_passage(self):
        """Ensure that a passage can be added to a reading"""
        row_count = readings_model.add_reading_to_db(self.example_reading["name"], self.example_reading["description"], self.example_reading["translation"])
        self.assertEqual(row_count, 1, "Can't add reading to DB")

        row_count = readings_model.add_more_passages(1, self.example_reading["passage"])
        self.assertEqual(row_count, 1, "Passage was not added to reading")

        passages = readings_model.find_reading_passages(1, self.example_reading["translation"])
        self.assertEqual(len(passages), 1, "Reading should have 1 passage associated with it")

        self.assertTrue(self.expected_passage in passages[self.example_reading["passage"]]["content"], "Genesis 1:1 did not return expected value from API")

class PostsTestCase(FlaskTestCase):

    example_reading = {
        "name": "Some reading",
        "description": "A description",
        "translation": "NKJV"
    }

    example_post = {
        "message": "Hi, this is a message",
        "user": 1,
        "originator_type": "reading",
        "originator_id": 1,
    }

    def setUp(self):
        super(PostsTestCase, self).setUp()
        # Use proxy user for these tests
        g.user = ProxyUser()

    def test_create_reading_post(self):
        """Test creating a discussion post on a reading"""
        row_count = readings_model.add_reading_to_db(self.example_reading["name"], self.example_reading["description"], self.example_reading["translation"])
        self.assertEqual(row_count, 1)

        # Create post on newly created reading
        row_count = posts_model.create_post(self.example_post["user"], self.example_post["message"], self.example_post["originator_type"], self.example_post["originator_id"])
        self.assertEqual(row_count, 1)

        # One post should be associated with the reading
        posts = readings_model.get_posts(self.example_post["originator_id"])
        self.assertEqual(len(posts), 1)

        # Make sure created post is the same as the initial data
        self.assertEqual(posts[0]["message"], self.example_post["message"])
        self.assertEqual(posts[0]["author"].user_id, self.example_post["user"])

class UsersTestCase(FlaskTestCase):

    example_user = {
        "email": "user@example.com",
        "first_name": "Fake",
        "last_name": "User",
        "password": "fakepassword123!"
    }

    def login(self, username, password):
        return self.client.post('/login/', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout/', follow_redirects=True)

    def test_register_user(self):
        """Ensure user model correctly registers the user"""
        user = users_model.register(self.example_user)

        self.assertTrue(user is not False, "User can't be created")

        self.assertEqual(user.first_name, self.example_user["first_name"], "Created user doesn't have correct first name")
        self.assertEqual(user.last_name, self.example_user["last_name"], "Created user doesn't have correct last name")
        self.assertEqual(user.username, self.example_user["email"], "Created user doesn't have correct email")

        self.assertTrue(user.check_password(self.example_user["password"]), "Created user doesn't have correct password")


    def test_login__logout_user(self):
        """Check that registered user can login and logout"""
        user = users_model.register(self.example_user)

        login = self.login(self.example_user["email"], self.example_user["password"])
        self.assertTrue(("Welcome " + self.example_user["first_name"]) in str(login.data), "User can't login")

        logout = self.logout()
        self.assertTrue("Logged out" in str(logout.data), "User can't logout")



if __name__ == '__main__':
    unittest.main()
