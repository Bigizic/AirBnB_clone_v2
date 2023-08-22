#!/usr/bin/python3
"""Unittest module for City() class
"""

from models.city import City
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from unittest.mock import patch
import time


class TestCity_method(unittest.TestCase):
    """Implementation
    """

    def setUp(self):
        self.city = City()

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.city.id))

    def test_city_inherits_from_base_model(self):
        self.assertIsInstance(self.city, BaseModel)

    def test_city_attributes_exist(self):
        self.assertTrue(hasattr(self.city, 'state_id'))
        self.assertTrue(hasattr(self.city, 'name'))

    def test_city_attributes_are_empty_strings_by_default(self):
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")

    def test_city_attributes_can_be_assigned(self):
        self.city.state_id = "2468"
        self.city.name = "los"

        self.assertEqual(self.city.state_id, "2468")
        self.assertEqual(self.city.name, "los")

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(City.state_id))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(City.name))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))


class TestCity_save_method(unittest.TestCase):
    """Unittests for testing save() for the class City
    """

    def test_city_updates_updated_at_attribute(self):
        city = City()
        initial_updated_at = city.updated_at
        time.sleep(1)
        city.save()
        new_updated_at = city.updated_at
        self.assertGreater(new_updated_at, initial_updated_at)


class TestCity_to_dict_method(unittest.TestCase):
    """Unittests for testing to_dict() for the class City
    """

    def setUp(self):
        self.city = City()
        self.city.state_id = "test@example.com"
        self.city.name = "password123"

    def test_to_dict_returns_dictionary(self):
        result = self.city.to_dict()
        self.assertIsInstance(result, dict)

    def test_to_dict_contains_expected_attributes(self):
        result = self.city.to_dict()

        self.assertIn('id', result)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)
        self.assertIn('state_id', result)
        self.assertIn('name', result)

    def test_to_dict_attribute_values_are_correct(self):
        result = self.city.to_dict()
        self.assertEqual(result['state_id'], "test@example.com")
        self.assertEqual(result['name'], "password123")


if __name__ == '__main__':
    unittest.main()
