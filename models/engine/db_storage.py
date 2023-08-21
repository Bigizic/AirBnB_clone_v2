#!/usr/bin/python3
"""A module that serves as the DataBase Engine
"""

import os
from models.city import City
from models.state import State
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import class_mapper


class DBStorage():
    """New Engine DBStorage for managing the database storage,
    interactions and relationships between different classes
    """
    __engine = None
    __session = None

    def __init__(self):
        """creates the engine self.__engine and session
        """
        hbnb_env = os.getenv('HBNB_ENV')
        user = os.getenv('HBNB_MYSQL_USER')
        p_wd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        d_b = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
                        'mysql+mysqldb://{}:{}@{}:3306/{}'
                        .format(user, p_wd, host, d_b),
                        pool_pre_ping=True)

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        if hbnb_env == 'test':
            metadata = MetaData(bind=self.__engine)
            metadata.reflect()
            metadata.drop_all()

    def all(self, cls=None):
        """query to the current database session(self.__session)
        """

        class_mapping = {
                'State': State,
                'City': City,
                'User': User,
                'Place': Place,
                'Review': Review,
                'Amenity': Amenity
                'BaseModel': BaseModel
            }

        objects = []
        if cls is None:
            for cls_name, cls_obj in class_mapping.items():
                objects += self.__session.query(cls_obj).all()
        else:
            objects = self.__session.query(cls).all()

        res = {f"{type(obj).__name__}.{obj.id}": obj for obj in objects}

        return res

    def new(self, obj):
        """add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)
        else:
            pass

    def reload(self):
        """reloads data from the database and creates a session
        """
        Base.metadata.create_all(self.__engine)
        temp_session = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(temp_session)
        self.__session = Session()

    def close(self):
        """closes Session
        """
        self.__session.close()
