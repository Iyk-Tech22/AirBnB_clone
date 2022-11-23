#!/usr/bin/python3
import cmd
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
		"""show command: show a specific instance of an obj base on the cls_name and cls_id"""
		def action(cls_name, cls_id, attr_name, attr_val):
			"get an instance from the file storage"
			self.storage.reload()
			objs = self.storage.all()
			found = False
			for key, value in objs.items():
				key = key.split(".")
				if cls_name in key and cls_id in key:
					print(value.__str__())
					found = True
					break
			if not found:
				print("** no instance found **")
		self.validate_cmd_arg(arg, action)

	def do_destroy(self, arg):
		"""destroy command: destroy an instance base on the class and id"""

		def action(cls_name, cls_id, attr_name, attr_val):
			"delete a instance and save to file"
			found = False
			self.storage.reload()
			objs = self.storage.all()
			for key in objs.keys():
				key_c = key.split(".")
				if cls_name in key_c and cls_id in key_c:
					del objs[key]
					self.storage.save()
					found = True
					break
			if not found:
				print("** no instance found **")
		self.validate_cmd_arg(arg, action)
	def do_all(self, arg):
		"""all / all option: Print all string representation of an instance base or do not have class name"""
		objs = self.storage.all()
		if not arg:
			print([value.__str__() for key, value in objs.items() if "BaseModel" in key.split(".")])
		elif arg in self.Classes_k:
			print([value.__str__() for key, value in objs.items() if arg in key.split(".")])
		else:
			print("** class doesn't exist **")

	def do_update(self, arg):
		""" update command: update an attribute or add new attribute to an instance
		    Usage: <class name> <id> <attribute name> "<attribute value>"
		"""
		def action(cls_name, cls_id, attr_name, attr_val):
			"update attr or add new attr at time"
			objs = self.storage.all()
			found = False
			for key, value in objs.items():
				key_c = key.split(".")
				if cls_name in key_c and cls_id in key_c:
					if not attr_name:
						print("** attribute name missing **")
					elif not attr_val:
						print("** value missing **")
					else:
						obj_to_update = value.to_dict()
						del objs[key]
						obj_to_update[attr_name] = attr_val
						obj_to_update = self.Classes[cls_name](**obj_to_update)
						obj_to_update.save()
					found = True
					break
			if not found:
				print("** no instance found **")
		self.validate_cmd_arg(arg, action)
		
	def do_quit(self, arg):
		"""Quit command to exit the program"""
		return True

	def do_EOF(self, arg):
		"""EOF command: quick when key event is fire with CtrlD"""
		return True

	def emptyline(self):
		"""Does nothing when the enterkey is pressed"""
		pass

	def validate_cmd_arg(self, arg, action):
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
				attr_name = args[2] if len(args) >= 3 else None
				attr_val = args[3] if len(args) == 4 else None
				action(cls_name, cls_id, attr_name, attr_val)

if __name__ == "__main__":
	HBNBCommand().cmdloop()
