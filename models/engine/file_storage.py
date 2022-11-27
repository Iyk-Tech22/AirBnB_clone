#!/usr/bin/python3
import datetime
import os
import json

"""
"""
class FileStorage:
    """
    This is a storage class in which all other files will be stored
    Attributes:
        __file_path (str): path to the file in which object is saved
        __oject (dict): a dictionaryof an instatiated object
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary reprsentation of __objects."""
        return FileStorage.__objects
    def new(self, obj):
        """
        This method is used to add a new object to the storage.
        Args:
            obj (object): an object to be added to the storage
        """
        clname = obj.__class__.__name__
        key = "{}.{}".format(clname, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path).
        """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            data = {key: value.to_dict() for key, value in FileStorage.__objects.items()}
            json.dump(data, f)

    def classes(self):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

        
    def reload(self):
        """
         deserializes the JSON file to __objects (only if the JSON file (__file_path) exists ; otherwise, do nothing. 
         If the file doesn’t exist, no exception should be raised)
        """
        if not os.path.isfile(FileStorage.__file_path):
            return

        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {key: self.classes()[value["__class__"]](**value)
                        for key, value in obj_dict.items()}
            FileStorage.__objects = obj_dict

        def attributes(self):
             """Returns the valid attributes and their types for classname"""
             attributes = {
                "BaseModel":
                        {"id": str,
                        "created_at": datetime.datetime,
                        "updated_at": datetime.datetime},
                "User":
                        {"email": str,
                        "password": str,
                        "first_name": str,
                        "last_name": str},
                "State":
                        {"name": str},
                "City":
                        {"state_id": str,
                        "name": str},
                "Amenity":
                        {"name": str},
                "Place":
                        {"city_id": str,
                        "user_id": str,
                        "name": str,
                        "description": str,
                        "number_rooms": int,
                        "number_bathrooms": int,
                        "max_guest": int,
                        "price_by_night": int,
                        "latitude": float,
                        "longitude": float,
                        "amenity_ids": list},
                "Review":
                {"place_id": str,
                            "user_id": str,
                            "text": str}
            }
        return attributes
