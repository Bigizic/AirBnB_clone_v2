#!/usr/bin/python3
"""Unittest module for state class
This module contains test for:
1.Test the type of the id is string.
2.Test the type of name is string.
3.Test two states have different created at.
4.Test two states have different updated at.
5.Test two states have different id.
6.Test the type of the created at is datetime.
7.Test the type of the updated at is datetime.
"""

import unittest
from models.state import State
from datetime import datetime
from models.base_model import BaseModel
import time


class Test_State_foundation(unittest.TestCase):
    """Foundation tests easiest test cases"""

    def test_id_type(self):
        self.assertEqual(str, type(State().id))

    def test_name_type(self):
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(str, type(State().name))

    def test_created_at_type(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_type(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_two_states_with_different_ids(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.id, s2.id)

    def test_two_states_with_different_created_at(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.created_at, s2.created_at)

    def test_two_states_with_diff_updated_at(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.updated_at, s2.updated_at)

    def test_state_inherits_from_base_model(self):
        s1 = State()
        self.assertIsInstance(s1, BaseModel)

    def test_state_attributes_exist(self):
        s1 = State()
        self.assertTrue(hasattr(s1, 'name'))

    def test_state_attributes_are_empty_strings_by_default(self):
        s1 = State()
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(s1.name, "")

    def test_state_attributes_can_be_assigned(self):
        s1 = State()
        s1.name = "Canada"
        self.assertEqual(s1.name, "Canada")

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_str(self):
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(str, type(State.name))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))


class TestState_save_method(unittest.TestCase):
    """Unittests for testing save() for the class State
    """

    def test_state_updates_updated_at_attribute(self):
        st = State()
        initial_updated_at = st.updated_at
        time.sleep(1)
        st.save()
        new_updated_at = st.updated_at
        self.assertGreater(new_updated_at, initial_updated_at)


class TestState_to_dict_method(unittest.TestCase):
    """Unittests for testing to_dict() for the class State
    """

    def setUp(self):
        self.st = State()
        self.st.name = "Canada"

        def test_to_dict_returns_dictionary(self):
            result = self.st.to_dict()
            self.assertIsInstance(result, dict)

        def test_to_dict_contains_expected_attributes(self):
            result = self.st.to_dict()

            self.assertIn('id', result)
            self.assertIn('created_at', result)
            self.assertIn('updated_at', result)
            self.assertIn('name', result)

        def test_to_dict_attribute_values_are_correct(self):
            result = self.st.to_dict()
            self.assertEqual(result['name'], "Canada")


if __name__ == '__main__':
    unittest.main()
