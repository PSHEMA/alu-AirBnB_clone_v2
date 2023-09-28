#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    # Relationship with City for DBStorage
    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete-orphan")

    # Getter attribute for FileStorage
    if getenv("HBNB_TYPE_STORAGE") == "file":
        @property
        def cities(self):
            """
            Returns a list of City instances with state_id equal to the current State.id.
            """
            from models import storage
            city_instances = storage.all("City")
            return [city for city in city_instances.values() if city.state_id == self.id]
