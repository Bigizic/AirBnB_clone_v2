#!/usr/bin/python3
"""Unittest module for user class

    1. inheritance test
    2. serialization and deserialization test
"""

import models
import unittest
from datetime import datetime
import time
from models.user import User
from models.base_model import BaseModel
from unittest.mock import patch


class TestUser_method(unittest.TestCase):
    """Implementations
    """

    def setUp(self):
        self.user = User()

    def test_user_inherits_from_base_model(self):
        self.assertIsInstance(self.user, BaseModel)

    def test_user_attributes_exist(self):
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'password'))
        self.assertTrue(hasattr(self.user, 'first_name'))
        self.assertTrue(hasattr(self.user, 'last_name'))

    def test_user_attributes_are_empty_strings_by_default(self):
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_attributes_can_be_assigned(self):
        self.user.email = "test@example.com"
        self.user.password = "password123"
        self.user.first_name = "John"
        self.user.last_name = "Doe"

        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))


class TestUser_save_method(unittest.TestCase):
    """Unittests for testing save() for the class User
    """

    def test_save_updates_updated_at_attribute(self):
        user = User()
        initial_updated_at = user.updated_at
        time.sleep(1)
        user.save()
        new_updated_at = user.updated_at
        self.assertGreater(new_updated_at, initial_updated_at)


class TestUser_to_dict_method(unittest.TestCase):
    """Unittests for testing to_dict() for the class User
    """

    def setUp(self):
        self.user = User()
        self.user.email = "test@example.com"
        self.user.password = "password123"
        self.user.first_name = "John"
        self.user.last_name = "Doe"

    def test_to_dict_returns_dictionary(self):
        # Call the to_dict() method
        result = self.user.to_dict()
        self.assertIsInstance(result, dict)

    def test_to_dict_contains_expected_attributes(self):
        result = self.user.to_dict()

        self.assertIn('id', result)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)
        self.assertIn('email', result)
        self.assertIn('password', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)

    def test_to_dict_attribute_values_are_correct(self):
        result = self.user.to_dict()

        self.assertEqual(result['email'], "test@example.com")
        self.assertEqual(result['password'], "password123")
        self.assertEqual(result['first_name'], "John")
        self.assertEqual(result['last_name'], "Doe")


if __name__ == '__main__':
    unittest.main()
