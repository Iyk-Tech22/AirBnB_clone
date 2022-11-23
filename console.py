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
	classes_k = storage.classes().keys()

	def postloop(self):
		"print a newline after exiting the console"
		print()

	def parseline(self, arg):
		"return tuple of the cmd and the args"
		res = cmd.Cmd.parseline(self, arg)
		return res

	def do_create(self, arg):
		"cmd to create a new instance of a class"
		if not arg:
			print("** class name missing **")
		elif arg not in self.classes_k:
			print("** class doesn't exist **")
		else:
			new_obj = BaseModel()
			new_obj.save()
			print(new_obj.id)

	def do_show(self, arg):
		"cmd to show a specific instance of an obj base on the cls_name and cls_id"
		cls_name, cls_id, cmd = self.parseline(arg)
		if not arg:
			print("** class name missing **")
		else:
			if cls_name not in self.classes_k:
				print("** class doesn't exist **")
			elif not cls_id:
				print("** instance id missing **")
			else:
				self.storage.reload()
				objs_v = self.storage.all().values()
				found = False
				for value in objs_v:
					obj_id = value.id.split("-")
					obj_clsName = str(value.__class__)
					if cls_name in obj_clsName and cls_id  in obj_id:
						print(value.__str__())
						found = True
				if not found:
					print("** no instance found **")

	def do_quit(self, arg):
	
		"Quit command to exit the program"
		return True

	def do_EOF(self, arg):
		return True

	def emptyline(self):
		"""Does nothing when the enterkey is pressed"""
		pass

if __name__ == "__main__":
	HBNBCommand().cmdloop()
