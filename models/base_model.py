#!bin/usr/python3

import uuid
from datetime import datetime
from models import storage

"""
this defines the base model where every other models will be 
built on.
"""

class BaseModel:
    """Base class for the airbn project where evry other class will depend
    this has public instance and uses uuid and datatime to set up the instances
    """ 
   
    def __init__(self, *rgs, **kwargs):
        """
        constructor, this method willdefine the basic constructorfor each
        instance.
        Args:
            *args (any): variale data type
            **kwargs (dict):key-value pairs of the attributes
        """
        datetimeform = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], datetimeform)
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], datetimeform)
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute updated_at"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary which consist of all keys/values of the __dict__"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict