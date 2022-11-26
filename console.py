#!/usr/bin/python3


import cmd
import re
from shlex import shlex
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage

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

    def onecmd(self, arg):
        """ onecmd is a func that is called by cmd.Cmd
            before the args  dispach to the right cmd
        """
        try:
            if "." in arg and ")" in arg:
                args = arg.split(".")
                cls_name = args[0]
                cls_id = ""
                attr_name = ""
                attr_val = ""
                res = args[1].strip(")").split("(")
                if len(res) == 1:
                    cmd_name = res[0]
                elif "," not in res[1] and len(res) == 2:
                    cmd_name = res[0]
                    cls_id = res[1].strip('"')
                else:
                    cmd_name = res[0]
                    res = res[1].split(",")
                    cls_id = res[0].replace('"', '')
                    attr_name = res[1]
                    attr_val = res[2]
                arg = f"{cmd_name} {cls_name} {cls_id} {attr_name} {attr_val}"
        finally:
            return cmd.Cmd.onecmd(self, arg)

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
                    obj_to_update = objs[key].to_dict()
                    del objs[key]
                    obj_to_update[attr_name] = attr_val
                    obj_to_update = self.Classes[cls_name](**obj_to_update)
                    obj_to_update.save()
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
