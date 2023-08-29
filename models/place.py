#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
import models
from models.review import Review
from sqlalchemy import Table
from models.amenity import Amenity

if models.storage_temp == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """  place to stay """
    __tablename__ = 'places'
    if models.storage_temp == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity",
                                 secondary="place_amenity",
                                 back_populates="place_amenities",
                                 viewonly=False)
        """
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     primary_key=True,
                                     nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'),
                                     primary_key=True,
                                     nullable=False))
        amenities = relationship("Amenity", secondary=place_amenity,
                                 back_populates="place_amenities",
                                 viewonly=False)
        """
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super().__init__(*args, **kwargs)

    if models.storage_temp != 'db':
        @property
        def reviews(self):
            """Getter attribute that retruns the list of Review
            instances with place_id equals to the current Place.id
            """
            instance_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    instance_list.append(review)
            return instance_list

        @property
        def amenities(self):
            """Getter attribute that retruns the list of Amenity
            intances based on the attribute amenity_ids that contains
            all Amenity.id linked to the place
            """
            instance_list = []
            for amenities in models.storage.all(Amenity).values():
                if amenities.id in self.amenity_ids:
                    instance_list.append(amenities)
            return instance_list

        @amenities.setter
        def amenities(self, amenity_obj):
            """Setter attribute that handles append method for adding
            an Amenity.id to the attribute amenity_ids. Accepts only
            Amenity objects
            """
            if isinstance(amenity_obj, Amenity):
                self.amenity_ids.append(amenities_obj.id)
