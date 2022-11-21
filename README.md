# Airbnb_clone: Console Project
The Console is very similar to the shell console. But it is narrow to a specific use case not as broad to as shell.
this console is design for devs uses. which is use for managing the backend of a project. giving devs the CRUD
funtionality of a project like:
* Create
* Modify
* Delete

The Console is a tool that is handy for backend devs. managing communication with the file storage and database
for persisting data.
## Commandline Intepriter:
A Commandline Intepriter is program that takes input as arguement and create process to execute those arguement.
Our Airbnb console is a commandline Intepriter that takes arguement and execute them. But it does create a process for executing does input. Instead it calls interface we defined in our classes to do specific operations. like creating User, show Data.....in File Storage or Database.
### Baisc Use of Airbnb Console:
there are to ways to use the Airbnb console
* Interactive mode
* Non interactive mode
#### Iteractive Mode
* **$./console.py** -> "the command"
* **(hbnb)** -> "Once the command has been executed this Displays the prompt" which wait for a command to be inputed then execute it and print the result of the input and display the prompt again. This process is called REPL (Read Execute Print Loop) this continue unitl a quit command is input to quit the Console. See Example Below
```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) help quit
Quit command to exit the program

(hbnb)
(hbnb) help create
Creates a new instance of class

(hbnb)
(hbnb) quit
$
```
#### Non Interactive Mode
```bash
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```
## Authors
* Uche Esere
* Iyk Faiz
