#!/usr/bin/python3
"""A uniitest moule for FileStorage class

This module contains test for:
    1. if the file is a .json extension
    2. if the new() creates the key for the dict and sets it in objects
        with the created key. Key should be in a specific format
    3. if the save() sucessfully serialize the objects and saves to the
        json file path
    4. if reload succesffuly reloads the objects from the json file and
        if it reloads it in the correct format
    5. if the new() succesfully creates objects for other classes, like:
        User
        City
        Amenity
        Place
        Reviews
        State
"""
import unittest


from models.engine.file_storage import FileStorage
from unittest.mock import patch, MagicMock
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from unittest.mock import patch
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
import json
import models


class Test_file_storage_foundations(unittest.TestCase):
    """File storage tests
    """

    # test if the file being created is a .json file
    def test_correct_file_extension(self):
        m_s = FileStorage()
        self.assertEqual(m_s._FileStorage__file_path.endswith('.json'), True)

    # test if the new() method returns the objects in the correct format
    def test_new_methods(self):
        my_store = FileStorage()
        obj = BaseModel()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)

    def test_file_path_attribute_is_none(self):
        file_storage = FileStorage()
        file_path = file_storage._FileStorage__file_path
        self.assertIsNotNone(file_path)

    # test if the save() serialzies the objects and saves it to the json
    # file path
    def test_save_method(self):
        my_store = FileStorage()
        obj = BaseModel()
        my_store.new(obj)
        my_store.save()

        # Opens the file for reading
        with open(my_store._FileStorage__file_path, "r") as open_file:
            data = open_file.read()
            # check if the data saved in the file path is not empty
            # returns truw as it's not equal to empty object
            self.assertNotEqual(data, "")

    # test if the reload() sucessfully reloads from the file path and
    # sets the __objects to the data it was able to read from the file

    def test_reload_method(self):
        my_store = FileStorage()
        obj = BaseModel()
        my_store.new(obj)
        my_store.save()
        my_store.reload()
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        cls_name = my_store._FileStorage__objects[key].__class__.__name__
        self.assertEqual(cls_name, "BaseModel")

    # test when new() is called upon User() class, if it outputs correct
    # format
    def test_new_user_method(self):
        my_store = FileStorage()
        obj = User()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)

    # test when new() is called upon State() class, if it outputs correct
    # format
    def test_new_state_method(self):
        my_store = FileStorage()
        obj = State()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)

    # test when new() is called upon City() class, if it outputs correct
    # format
    def test_new_city_method(self):
        my_store = FileStorage()
        obj = City()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)

    # test when new() is called upon Amenity() class, if it outputs correct
    # format
    def test_new_amenity_method(self):
        my_store = FileStorage()
        obj = Amenity()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)

    # test when new() is called upon Place() class, if it outputs correct
    # format
    def test_new_place_method(self):
        my_store = FileStorage()
        obj = Place()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)

    # test when new() is called upon Review() class, if it outputs correct
    # format
    def test_new_review_method(self):
        my_store = FileStorage()
        obj = Review()
        my_store.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertEqual(key in my_store._FileStorage__objects, True)
        self.assertEqual(my_store._FileStorage__objects[key], obj)


class TestFileStorage_all_method(unittest.TestCase):
    """all() method test case
    """

    def test_all_returns_dictionary(self):
        file_storage = FileStorage()
        result = file_storage.all()
        self.assertIsInstance(result, dict)


class TestFileStorage_new_method(unittest.TestCase):
    """new() method test case
    """

    def test_new_adds_object_to_objects_dictionary(self):
        file_storage = FileStorage()
        bm = BaseModel()
        file_storage.new(bm)
        o_b = file_storage.all()

        self.assertIn(f"{bm.__class__.__name__}.{bm.id}", o_b)
        self.assertEqual(o_b[f"{bm.__class__.__name__}.{bm.id}"], bm)


class TestFileStorage_save_method(unittest.TestCase):
    """save() method test case
    """

    def test_save_calls_json_dump(self):
        file_storage = FileStorage()
        with patch('builtins.open') as mock_open, \
                patch('json.dump') as mock_json_dump:
            file_storage.save()

            obj = file_storage._FileStorage__file_path
            mock_open.assert_called_once_with(obj, 'w')
            mock_json_dump.assert_called_once()


class TestFileStorage_reload_method(unittest.TestCase):
    """reload() method test cases
    """

    def test_reload_calls_json_load(self):
        file_storage = FileStorage()
        with patch('builtins.open') as mock_open, \
                patch('json.load') as mock_json_load:
            mock_file = MagicMock()

            mock_open.return_value.__enter__.return_value = mock_file
            file_storage.reload()
            oh = file_storage._FileStorage__file_path
            mock_open.assert_called_once_with(oh, 'r')
            mock_json_load.assert_called_once_with(mock_file)


if __name__ == '__main_':
    unittest.main()
