#!/usr/bin/python3

import cmd
import re
from shlex import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.errors import *
from models.engine.file_storage import FileStorage
from datetime import datetime

"""
Console is the main entry for the program.
takes in specific commnad and execute them
you can manage the object stored in file and database
from the console.
"""


class HBNBCommand(cmd.Cmd):
    "subclass inheriting from cmd module"
    prompt = "(hbnb) "
    storage = FileStorage()
    Classes = storage.classes()
    Classes_k = storage.classes().keys()

    def postloop(self):
        "print a newline after exiting the console"
        print()

    def parseline(self, arg):
        "return tuple of the cmd and the args"
        res = cmd.Cmd.parseline(self, arg)
        return res

    def do_create(self, arg):
        """create command: to create a new instance of a class"""
        if not arg:
            print("** class name missing **")
        elif arg not in self.Classes_k:
            print("** class doesn't exist **")
        else:
            new_obj = self.Classes[arg]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, arg):
        """show command: show instance base on the cls_name and cls_id"""
        def action(cls_name, cls_id, attr_name, attr_val):
            "get an instance from the file storage"
            objs = self.storage.all()
            key = f"{cls_name}.{cls_id}"
            if key in objs.keys():
                print(objs[key])
            else:
                print("** no instance found **")
        self.validate_arg(arg, action)

    def do_destroy(self, arg):
        """destroy command: destroy an instance base on the class and id"""

        def action(cls_name, cls_id, attr_name, attr_val):
            "delete a instance and save to file"
            objs = self.storage.all()
            key = f"{cls_name}.{cls_id}"
            if key in objs.keys():
                del objs[key]
                self.storage.save()
            else:
                print("** no instance found **")
        self.validate_arg(arg, action)

    def do_all(self, arg):
        """all opt: Print all str repr of an
           instance base or do not have class name
        """
        objs = self.storage.all()
        if not arg:
            print([value.__str__() for key,
                   value in objs.items()])
        elif arg in self.Classes_k:
            print([value.__str__() for key,
                   value in objs.items() if arg in key.split(".")])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """ update command: update an attr or add new attr to an instance
            Usage: <class name> <id> <attribute name> "<attribute value>"
        """
        def action(cls_name, cls_id, attr_name, attr_val):
            "update attr or add new attr at time"
            objs = self.storage.all()
            key = f"{cls_name}.{cls_id}"
            if key in objs.keys():
                if not attr_name:
                    print("** attribute name missing **")
                elif not attr_val:
                    print("** value missing **")
                else:
                    try:
                        obj = objs[key]
                        vtype = type(attr_name)
                        obj.__dict__[attr_name] = vtype(attr_val)
                    except KeyError:
                        obj.__dict__[attr_name] = attr_val
                    finally:
                        obj.updated_at = datetime.utcnow()
                        self.storage.save()
            else:
                print("** no instance found **")
        self.validate_arg(arg, action)

    def do_count(self, arg):
        """count command: count the numbers of instances"""
        objs = self.storage.all()
        count = 0
        if not arg:
            for i in objs:
                count += 1
            print(count)
        elif arg in self.Classes_k:
            for key in objs.keys():
                if arg in key.split("."):
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command: quick when key event is fire with CtrlD"""
        return True

    def emptyline(self):
        """Does nothing when the enterkey is pressed"""
        pass

    def validate_arg(self, arg, action):
        """validate the args of show, destroy....commands"""
        cls_name, cls_id, args = self.parseline(arg)
        if not arg:
            print("** class name missing **")
        else:
            if cls_name not in self.Classes_k:
                print("** class doesn't exist **")
            elif not cls_id:
                print("** instance id missing **")
            else:
                args = args.split(" ")
                cls_name = args[0]
                cls_id = args[1]
                if len(args) >= 3:
                    attr_name = args[2]
                else:
                    attr_name = None
                if len(args) >= 4:
                    attr_val = args[3]
                else:
                    attr_val = None
                action(cls_name, cls_id, attr_name, attr_val)

    def Handler(self, arg):
        """
           Handles other commands
           [Usage]: <class>.<method>...User.all()
        """
        printable = ("all(", "create(", "count(", "show(")
        try:
            result = eval(arg)
            for i in printable:
                if i in arg:
                    print(result)
                    break
        except AttributeError:
            print("*** Invalid Method ***")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError:
            print("** instance id missing **")
        except FieldMissingError:
            print("** fields missing **")
        except Exception:
            print("** invalid syntax **")

    def default(self, arg):
        """ Calls handler"""
        if "." in arg and ")" in arg[-1]:
            if arg.split(".")[0] in self.Classes_k:
                return self.Handler(arg)
            else:
                print("** class doesn't exist **")
                return
        else:
            return cmd.Cmd.default(self, arg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
