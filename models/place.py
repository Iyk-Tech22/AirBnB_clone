#!/usr/bin/python3
"""
"""
from models.base_model import BaseModel


class Place (BaseModel):
    """
    inherits from BaseModel
    """
    city_id = " "
    user_id = " "
    name = " "
    description = " "
    number_roomsInt = 0
    number_bathrooms: int = 0
    max_quest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity = []
