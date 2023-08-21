#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
import models
from models.base_model import Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    if models.storage_temp == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super().__init__(*args, **kwargs)
