#!/usr/bin/python3
""" """

import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the Database Storage Engine.
        Create the engine (self.__engine) and configure it.
        Create the session (self.__session).
        """
        db_user = os.getenv("HBNB_MYSQL_USER")
        db_pwd = os.getenv("HBNB_MYSQL_PWD")
        db_host = os.getenv("HBNB_MYSQL_HOST", default="localhost")
        db_name = os.getenv("HBNB_MYSQL_DB")

        self.__engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{db_user}:{db_pwd}@{db_host}/{db_name}",
            pool_pre_ping=True
        )

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def all(self, cls=None):
        """
        Get all objects depending on the class name (cls).
        If cls is None, query all types of objects.
        Returns a dictionary with object_id as the key and object as the value.
        """
        from models import classes

        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """
        Add the object to the current database session.
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete obj from the current database session if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and create the current session.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """
        Close the current session.
        """
        self.__session.close()
