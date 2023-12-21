#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)

class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'
    
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    @property
    def amenities(self):
        """Getter attribute that returns a list of Amenity objects based on the amenity_ids attribute"""
        from models import storage
        amenity_objects = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        return amenity_objects

    @amenities.setter
    def amenities(self, amenity):
        """Setter attribute that adds an Amenity object's id to the amenity_ids attribute"""
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)

    @property
    def reviews(self):
        """Getter attribute that returns the list of Review instances
        with place_id equal to the current Place.id"""
        from models import storage
        reviews_list = []
        for review in storage.all("Review").values():
            if review.place_id == self.id:
                reviews_list.append(review)
        return reviews_list
