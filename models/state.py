#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy


class State(BaseModel, Base):
    """ State class """
    if models.storage_temp == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super().__init__(*args, **kwargs)

    if models.storage_temp != 'db':
        @property
        def cities(self):
            """Getter method for cities
            """
            cities = []
            for city_id, city_obj in models.storage.all(City).items():
                if city_obj.state_id == self.id:
                    cities.append(city_obj)
            return cities
