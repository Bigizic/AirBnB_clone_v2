#!/usr/bin/python3
"""A Class Module
a class FileStorage that serializes instances to a JSON file and
deserializes JSON file to instances

Args:
    None

Return:
    None

Raises:
    Void
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """FileStorage implementation
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns all objects
        """
        if cls is None:
            return self.__objects
        else:
            cls_obj = {k: obj for k, obj in self.__objects.items()
                       if isinstance(obj, cls)}
            return cls_obj

    def new(self, obj):
        """Creates the key for the dict and sets in __objects the obj
            with the created key
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj
        else:
            return {}

    def save(self):
        """Serializes the __objects to the JSON file path
        """
        with open(self.__file_path, "w") as open_file:
            data = {key: obj.to_dict() for key, obj in
                    self.__objects.items()}
            json.dump(data, open_file)

    def reload(self):
        """Reloads data from the file and deserialize the data it read
        """
        try:
            with open(self.__file_path, "r") as open_file:
                data = json.load(open_file)
                for key, val in data.items():
                    val = eval(val["__class__"])(**val)
                    self.__objects[key] = val
        except Exception:
            pass

    def delete(self, obj=None):
        """elete obj from __objects if it’s inside otherwise
        does nothing
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)
        else:
            pass
