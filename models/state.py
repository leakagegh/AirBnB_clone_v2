#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def cities(self):
        from models.storage import FileStorage
        cities = []
        for city in FileStorage().all(cls=City).values():
            if city.state_id == self.id:
                cities.append(city)
        return cities
