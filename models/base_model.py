#!bin/usr/python3

import uuid
from models.engine.errors import *
from datetime import datetime
from models import storage
from models import FileStorage
from datetime import datetime

"""
this defines the base model where every other models will be
built on.
"""


class BaseModel:
    """Base class for the airbn project where evry other class will depend
    this has public instance and uses uuid and datatime to set up the instances
    """
    FileStorage = FileStorage()

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
            storage.new(self)
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
        """returns a dict which consist of all keys/values of the __dict__"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict

    @classmethod
    def all(cls):
        """ print all instance of a class """
        objs = cls.FileStorage.all()
        results = []
        for key, val in objs.items():
            if key.startswith(cls.__name__):
                results.append(str(val))
        return (results)

    @classmethod
    def create(cls, *args, **kwargs):
        """create a new instance and save to file"""
        inst = cls(args, kwargs)
        return (inst.id)

    @classmethod
    def count(cls):
        """count all instance of a class"""
        objs = cls.FileStorage.all()
        count = 0
        for key in objs.keys():
            if cls.__name__ in key.split("."):
                count += 1
        return (count)

    @classmethod
    def show(cls, iid):
        objs = cls.FileStorage.all()
        key = f"{cls.__name__}.{iid}"
        if not objs.get(key):
            raise InstanceNotFoundError
        return (objs[key])

    @classmethod
    def destroy(cls, iid):
        objs = cls.FileStorage.all()
        key = f"{cls.__name__}.{iid}"
        if not objs.get(key):
            raise InstanceNotFoundError
        del objs[key]
        cls.FileStorage.save()

    @classmethod
    def update(cls, *args):
        """update a value of an instance"""
        objs = cls.FileStorage.all()
        key = f"{cls.__name__}.{args[0]}"
        if not objs.get(key):
            raise InstanceNotFoundError
        elif len(args) == 1:
            raise FieldMissingError
        elif len(args) == 2 and not isinstance(args[1], dict):
            print("** value missing **")
        else:
            obj = objs[key]
            if isinstance(args[1], dict):
                argv = args[1].items()
            else:
                argv = [args[1:3]]
            for arg in argv:
                try:
                    key, value = arg
                    vtype = type(obj.__dict__[key])
                    obj.__dict__[key] = vtype(value)
                except KeyError:
                    obj.__dict__[key] = value
                finally:
                    obj.updated_at = datetime.utcnow()
                    cls.FileStorage.save()
