#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
import models
from models.base_model import Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    if models.storage_temp == 'db':
        place_id = Column(String(60), ForeignKey('places.id'),
                          nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super().__init__(*args, **kwargs)
