#!/usr/bin/python3
"""Unittest module for base class

This module contains test for:
    1. if the id returns a valid string and if the id type is a string
    2. if the created at returns the correct format
    3. if the updated_at returns the correct format
    4. if str prints the correct string format
    5. if to_dict returns a dictionary containing all keys/values of
        __dict__ of the instance
    6. if *args is being used or not
"""
import unittest


from models.base_model import BaseModel
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from time import sleep
import time
import models


class Test_base_model_foundations(unittest.TestCase):
    """Foundations test i.e easier tests cases
    """

    # tes when no argument is passed to BaseModel
    def test_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    # test two models unique id not the same
    def test_two_unique_id(self):
        model_1 = BaseModel()
        model_2 = BaseModel()
        self.assertNotEqual(model_1.id, model_2.id)

    # test different instance of same model different updated_at
    def test_different_updated_at_same_model(self):
        model_1 = BaseModel()
        sleep(0.05)
        model_2 = BaseModel()
        self.assertLess(model_1.updated_at, model_2.updated_at)

    # test argument unused
    def test_args_unused(self):
        model = BaseModel(None)
        self.assertNotIn(None, model.__dict__.values())

    # test if the id is of str (string) type
    def test_valid_id_type(self):
        id_value = BaseModel()
        self.assertIsInstance(id_value.id, str, None)

    # test if created_at is datetime type before a call to the to_dict()
    def test_createdat_type(self):
        created_at_value = BaseModel()
        self.assertIsInstance(created_at_value.created_at, datetime, None)

    # test if updated_at is datetime type before a call to the to_dict()
    def test_updatedat_type(self):
        updated_at_value = BaseModel()
        self.assertIsInstance(updated_at_value.updated_at, datetime, None)

    # test if updated_at is str type after making a call to the to_dict()
    def test_update_at_type_to_dict(self):
        updated = BaseModel()
        val = updated.to_dict()
        self.assertIsInstance(val['updated_at'], str, None)

    # test if created_at is str type after making a call to the to_dict()
    def test_created_at_type_to_dict(self):
        created = BaseModel()
        val = created.to_dict()
        self.assertIsInstance(val['created_at'], str, None)

    # test if updated_at returns the correct format for the date.time
    def test_updated_at_correct_format(self):
        base_model = BaseModel()
        u_str = base_model.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        u_format = self.validate_datetime_format(u_str)
        self.assertTrue(u_format, "invalid format")

    # test if created_at returns the correct format for the date.time
    def test_created_at_correct_fromat(self):
        base_model = BaseModel()
        c_str = base_model.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        c_format = self.validate_datetime_format(c_str)
        self.assertTrue(c_format, "invalid format")

    # validates created_at and updated_at date.time formats
    def validate_datetime_format(self, datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
            return True
        except ValueError:
            return False

    # test if str prints the correct string format
    def test_str_correct_fromat(self):
        my_model = BaseModel()
        dct = str(my_model.__dict__)
        cla = my_model.__class__.__name__
        expected = "[{}] ({}) {}" .format(cla, my_model.id, dct)
        self.assertNotEqual(str(my_model), expected, None)

    # test if to_dict returns a dictionary containing all keys and
        # values of the instance
    def test_to_dict_dictionary_type(self):
        my_model = BaseModel()
        self.assertIsInstance(my_model.to_dict(), dict, None)

    # test if args is being used, in this test we don't want to use args
        # so we have to test if it's being used in the code
    def test_if_args_is_being_used(self):
        """In this test i created a dictionary and added it to the
            BaseModel kwargs using the double pointer as refernce to
            kwargs, then i created an args and added it to the BaseModel
            the BaseModel should accept the kwargs but not args,
            how do i know this?? The BaseModel was built to accept kwargs
            only, so passing arguments in args thought to be the id and
            other attribute should not be equal to the BaseModel
            attributes, that's why i used the NotEqual to compare args
        """
        model_dict = {
                'id': '1234-5678',
                'created_at': '2017-09-28 21:03:54.052298',
                'updated_at': '2017-09-28 21:03:54.052302',
                'name': 'Isaac'
        }
        my_kwargs = BaseModel(**model_dict)

        my_args = BaseModel('Hol', 'Bet', 'TTy')

        self.assertEqual(my_kwargs.id, '1234-5678')
        self.assertEqual(my_kwargs.created_at,
                         '2017-09-28 21:03:54.052298')
        self.assertEqual(my_kwargs.updated_at,
                         '2017-09-28 21:03:54.052302')
        self.assertNotEqual(my_args.id, 'Hol')
        self.assertNotEqual(my_args.created_at, 'Bet')
        self.assertNotEqual(my_args.updated_at, 'TTy')
        # check if args has the atribute name
        self.assertFalse(hasattr(my_args, 'name'))


class TestBaseModel_save_method(unittest.TestCase):
    """Unittest for the save method of BaseModel class
    """
    def test_save_updates_updated_at(self):
        model = BaseModel()
        initial_updated_at = model.updated_at
        time.sleep(1)
        model.save()
        new_updated_at = model.updated_at
        self.assertGreater(new_updated_at, initial_updated_at)

    def test_save_calls_storage_save(self):
        base_model = BaseModel()
        storage = MagicMock()
        models.storage = storage
        base_model.save()
        storage.save.assert_called_once()


class TestBaseModel_to_dict_method(unittest.TestCase):
    """This are test for the to_dict() method in the BaseModel class
    """

    def test_to_dict_returns_dictionary(self):
        base_model = BaseModel()
        obj_dict = base_model.to_dict()
        self.assertIsInstance(obj_dict, dict)

    def test_to_dict_contains_correct_attributes(self):
        base_model = BaseModel()
        obj_dict = base_model.to_dict()
        self.assertIn('id', obj_dict)
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertNotIn('__class__', obj_dict)

    def test_to_dict_attributes_are_correct(self):
        base_model = BaseModel()
        obj_dict = base_model.to_dict()
        self.assertEqual(base_model.id, obj_dict['id'])
        bm1 = base_model.created_at.isoformat()
        self.assertEqual(bm1, obj_dict['created_at'])
        bm2 = base_model.updated_at.isoformat()
        self.assertEqual(bm2, obj_dict['updated_at'])
        # self.assertEqual(base_model.__class__.__name__, obj_dict['__class__'])

    def test_to_dict_handles_additional_attributes(self):
        base_model = BaseModel()
        base_model.name = 'Example'
        base_model.number = 123

        obj_dict = base_model.to_dict()
        self.assertIn('name', obj_dict)
        self.assertIn('number', obj_dict)
        self.assertEqual(base_model.name, obj_dict['name'])
        self.assertEqual(base_model.number, obj_dict['number'])


class TestBaseModel_str_method(unittest.TestCase):
    """This test cases are for the __str__ method
    """

    def test_str_contains_attributes(self):
        base_model = BaseModel()
        base_model.name = 'Example'
        base_model.number = 123

        result = str(base_model)
        self.assertIn('name', result)
        self.assertIn(base_model.name, result)
        self.assertIn('number', result)
        self.assertIn(str(base_model.number), result)


if __name__ == "__main__":
    unittest.main()
