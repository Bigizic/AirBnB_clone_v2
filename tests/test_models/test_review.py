#!/usr/bin/python3
"""Unittest module for review()

    1. to_dict
    2. save
    3. serialization and deserialization
"""

import models
import unittest
from datetime import datetime
import time
from models.review import Review
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from unittest.mock import patch
import json
from models import storage
from unittest.mock import patch, MagicMock
from console import HBNBCommand
from io import StringIO
from time import sleep
import os


class TestReview_method(unittest.TestCase):
    """Implementations
    """

    def setUp(self):
        self.review = Review()

    def test_review_inherits_from_base_model(self):
        self.assertIsInstance(self.review, BaseModel)

    def test_to_dict_returns_dictionary(self):
        result = self.review.to_dict()
        self.assertIsInstance(result, dict)

    def test_to_dict_contains_expected_attributes(self):
        result = self.review.to_dict()
        self.assertIn("id", result)
        self.assertIn("created_at", result)
        self.assertIn("updated_at", result)
        self.assertIn("__class__", result)

    def test_to_dict_attribute_values_are_correct(self):
        self.review.place_id = "234567"
        self.review.user_id = "234567"
        self.review.text = "This is a review."

        result = self.review.to_dict()
        self.assertEqual(result['place_id'], "234567")
        self.assertEqual(result['user_id'], "234567")
        self.assertEqual(result['text'], "This is a review.")


class TestReviewsave_method(unittest.TestCase):
    """Unittests for testing save() for the class Review
    """

    def test_review_updates_updated_at_attribute(self):
        review = Review()
        initial_updated_at = review.updated_at
        time.sleep(1)
        review.save()
        new_updated_at = review.updated_at
        self.assertGreater(new_updated_at, initial_updated_at)


class TestReviewAttributes(unittest.TestCase):
    """Checks if review public attributes are set to None
    """

    def test_attributes_are_none(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_args_unused(self):
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def test_save_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def test_to_dict_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)

    def test_attributes_all_none(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.place_id(None)
            rv.user_id(None)
            rv.text(None)

class TestReview_to_dict_method(unittest.TestCase):
    """Unittests for testing to_dict() for the class Review
    """

    def setUp(self):
        self.review = Review()
        self.review.place_id = "456789"
        self.review.user_id = "fce12f8a"
        self.review.text = "proper"

    def test_to_dict_returns_dictionary(self):
        result = self.review.to_dict()
        self.assertIsInstance(result, dict)

    def test_to_dict_contains_expected_attributes(self):
        result = self.review.to_dict()

        self.assertIn('id', result)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)
        self.assertIn('place_id', result)
        self.assertIn('user_id', result)
        self.assertIn('text', result)

    def test_to_dict_attribute_values_are_correct(self):
        result = self.review.to_dict()
        self.assertEqual(result['place_id'], "456789")
        self.assertEqual(result['user_id'], "fce12f8a")
        self.assertEqual(result['text'], "proper")

    def test_serialization_and_deserialization(self):
        self.review.place_id = "2345667"
        self.review.user_id = "234567"
        self.review.text = "This is a review."
        serialized_review = json.dumps(self.review.to_dict())
        deserialized_review_dict = json.loads(serialized_review)
        deserialized_review = Review(**deserialized_review_dict)
        self.assertEqual(deserialized_review.place_id, self.review.place_id)
        self.assertEqual(deserialized_review.user_id, self.review.user_id)
        self.assertEqual(deserialized_review.text, self.review.text)


class TestReview_update_method(unittest.TestCase):
    """Lets update our review
    """

    def setUp(self):
        user = User()
        place = Place()
        self.user_idf = user.id
        self.place_idf = place.id

        self.review = Review()
        self.review.user_id = self.user_idf
        self.review.place_id = self.place_idf
        self.review.text = "Good resturant"

    def test_confirm_review(self):
        result = self.review.to_dict()
        self.assertEqual(result['user_id'], self.user_idf)
        self.assertEqual(result['place_id'], self.place_idf)
        self.assertEqual(result['text'], self.review.text)

    def test_update_review(self):
        self.review.text = None
        new_text = "Very good resturant"
        self.review.text = new_text
        result = self.review.to_dict()
        self.assertEqual(result['text'], self.review.text)

    def test_review_is_instance(self):
        self.assertIsInstance(self.review, BaseModel)

    def test_review_valid_inheritance_with_BaseModel(self):
        review = self.review.to_dict()
        self.assertIn('id', review)
        self.assertIn('created_at', review)
        self.assertIn('updated_at', review)


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rv))
        self.assertNotIn("place_id", rv.__dict__)

    def test_user_id_is_public_class_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rv))
        self.assertNotIn("user_id", rv.__dict__)

    def test_text_is_public_class_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rv))
        self.assertNotIn("text", rv.__dict__)

    def test_two_reviews_unique_ids(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_two_reviews_different_created_at(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_two_reviews_different_updated_at(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rvstr = rv.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_args_unused(self):
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rv.id, "345")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def test_two_saves(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rv.save()
        self.assertLess(second_updated_at, rv.updated_at)

    def test_save_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        rv = Review()
        self.assertIn("id", rv.to_dict())
        self.assertIn("created_at", rv.to_dict())
        self.assertIn("updated_at", rv.to_dict())
        self.assertIn("__class__", rv.to_dict())

    def test_to_dict_contains_added_attributes(self):
        rv = Review()
        rv.middle_name = "Holberton"
        rv.my_number = 98
        self.assertEqual("Holberton", rv.middle_name)
        self.assertIn("my_number", rv.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(rv.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        rv = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == '__main__':
    unittest.main()
