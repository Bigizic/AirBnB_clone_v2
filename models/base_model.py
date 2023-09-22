#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

if models.storage_temp == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if models.storage_temp == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow,
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow,
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if (key == 'created_at' or key == 'updated_at'):
                    setattr(self, key, datetime.strptime(value,
                            '%Y-%m-%d %H:%M:%S.%f'))
                elif key == '__class__':
                    setattr(self, key, type(self))
                else:
                    setattr(self, key, value)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            if kwargs.get("created_at", None) is None:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) is None:
                self.updated_at = datetime.now()

        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        """
        kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                 '%Y-%m-%d %H:%M:%S.%f')
        kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                 '%Y-%m-%d %H:%M:%S.%f')
        """
        # del kwargs['__class__']
        self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.to_dict())

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        clean_dictionary = {k: v for k, v in dictionary.items() if
                            k != '_sa_instance_state' and
                            k != '__class__'}
        return clean_dictionary

    def delete(self):
        """delete the current instance from the storage
        """
        models.storage.delete(self)
