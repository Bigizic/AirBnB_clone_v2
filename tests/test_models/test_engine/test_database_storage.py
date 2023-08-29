#!/usr/bin/python3
"""Unittests for DBStorage class of AirBnb_Clone_v2"""
import unittest
import os
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import MySQLdb
from datetime import datetime


class TestStatesobject(unittest.TestCase):
    """Unittest for the state object using mysqldb
    """

    @classmethod
    def setUp(self):
        """Handles connection to MySQLdb
        """
        if os.getenv("HBNB_ENV") == 'test':
            self.user_name = os.getenv("HBNB_MYSQL_USER")
            self.ps_wd = os.getenv("HBNB_MYSQL_PWD")
            self.d_b = os.getenv("HBNB_MYSQL_DB")
            my_host = os.getenv("HBNB_MYSQL_HOST")

        if os.getenv("HBNB_TYPE_STORAGE") == 'db':
            self.conn = MySQLdb.connect(host=my_host, port=3306,
                                        user=self.user_name,
                                        passwd=self.ps_wd,
                                        db=self.d_b, charset="utf8")
            self.cursor = self.conn.cursor()

    @classmethod
    def tearDown(self):
        """Closes connections
        """
        while self.cursor.nextset():
            #self.conn.next_result()
            pass
        self.cursor.close()
        self.conn.close()

    def test_create_state(self):
        """
        This test selects all from states table of the
        database and creates a state and check if there's
        an increment in the states table before and after
        creation
        """
        queries = """
        USE {};
        CREATE TABLE IF NOT EXISTS states (
            id INT,
            name VARCHAR(256) NOT NULL,
            PRIMARY KEY (id)
        );
        """.format(self.d_b)
        self.cursor.execute(queries)
        now = datetime.utcnow()
        formatted_datetime = now.strftime('%Y-%m-%d-%H:%M:%S.%f')

        q = "INSERT INTO states(id, name, created_at) VALUES (1, 'Lagos', {}),".format("2023-08-23-15-30-45-123456")
        self.cursor.execute(q)
        updated_count = len(self.cursor.fetchall())

        select_query = "SELECT * FROM states"
        self.cursor.execute(select_query)
        first_count = len(self.cursor.fetchall())

        sec_query = "INSERT INTO states (id, name) VALUES (5 'Georgia');"
        self.cursor.execute(sec_query)
        self.conn.commit()

        udpated_query = "SELECT * FROM states"
        self.cursor.execute(updated_query)
        updated_count = len(self.cursor.fetchall())

        self.assertNotEqual(first_count, updated_count)


if __name__ == "__main__":
    unittest.main()
