#!/usr/bin/python3
"""Unittest module for user class

    1. inheritance test
    2. serialization and deserialization test
"""

import models
import os
import unittest
from datetime import datetime
import time
from models.amenity import Amenity
from models.base_model import BaseModel
from unittest.mock import patch
import os


class TestAmenity_method(unittest.TestCase):
    """Implementations
    """

    def setUp(self):
        self.am = Amenity()

    def test_amenity_inherits_from_base_model(self):
        self.assertIsInstance(self.am, BaseModel)

    def test_amenity_attributes_exist(self):
        self.assertTrue(hasattr(self.am, 'name'))

    def test_amenity_attributes_are_empty_strings_by_default(self):
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(self.am.name, "")

    def test_amenity_attributes_can_be_assigned(self):
        self.am.name = "john"
        self.assertEqual(self.am.name, "john")

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_last_name_is_public_str(self):
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(str, type(Amenity.name))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))


class TestAmenity_save_method(unittest.TestCase):
    """Unittests for testing save() for the class Amenity
    """

    def test_amenity_updates_updated_at_attribute(self):
        am = Amenity()
        initial_updated_at = am.updated_at
        time.sleep(1)
        am.save()
        new_updated_at = am.updated_at
        self.assertGreater(new_updated_at, initial_updated_at)


class TestAmenity_to_dict_method(unittest.TestCase):
    """Unittests for testing to_dict() for the class Amenity
    """

    def setUp(self):
        self.am = Amenity()
        self.am.name = "isaac"

    def test_to_dict_returns_dictionary(self):
        result = self.am.to_dict()
        self.assertIsInstance(result, dict)

    def test_to_dict_contains_expected_attributes(self):
        result = self.am.to_dict()

        self.assertIn('id', result)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)
        self.assertIn('name', result)

    def test_to_dict_attribute_values_are_correct(self):
        result = self.am.to_dict()

        self.assertEqual(result['name'], "isaac")


if __name__ == '__main__':
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        unittest.main()
