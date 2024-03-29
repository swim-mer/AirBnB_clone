#!/usr/bin/python3
''' This module contains the entry point of the command interpreter.
'''
import cmd
import inspect
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    ''' Define commands for HBNB CLI. '''
    prompt = '(hbnb) '

    def do_quit(self, line):
        ''' Quit command to exit the program. '''
        return True

    def do_EOF(self, line):
        ''' Exit the program. '''
        return True

    def emptyline(self):
        ''' Do nothing if empty line is entered. '''
        pass

    def do_create(self, line):
        ''' Create new instance of a class, save it, and print its id.

            USAGE: create [OBJ TYPE]

            [OBJ TYPE] is a required argument that can be any of the following:
                BaseModel, User, State, City, Place, Amenity, Review.
        '''
        if line:
            try:
                new_ins = eval(line)()
                models.storage.new(new_ins)
                models.storage.save()
                print(new_ins.id)
            except NameError:
                print("** class doesn't exist **")
        else:
            print('** class name missing **')

    def do_show(self, line):
        ''' Get string representation of instance by its id.

            USAGE: show [OBJ TYPE] [OBJ ID]

            [OBJ TYPE] is a required argument that can be any of the following:
                BaseModel, User, State, City, Place, Amenity, Review.
            [OBJ ID] is a required argument and is the object's id, which can
                be accessed via <instance name>.id.
        '''
        if line == '':
            print("** class name missing **")
        else:
            args = line.split(' ')
            try:
                var = eval(args[0])()
                var_key = var.__class__.__name__ + '.' + var.id
                del models.storage._FileStorage__objects[var_key]
                models.storage.save()

            except NameError:
                print("** class doesn't exist **")
                return
            try:
                args[1]
            except IndexError:
                print("** instance id missing **")
                return
            try:
                models.storage._FileStorage__objects[args[0] + '.' + args[1]]
            except KeyError:
                print("** no instance found **")
                return
            else:
                if (args[0] + '.' + args[1]) in \
                 models.storage._FileStorage__objects:
                    print(models.storage._FileStorage__objects[args[0] + '.' +
                          args[1]])

    def do_destroy(self, line):
        ''' Delete instance of a given class.

            USAGE: destroy [OBJ TYPE] [OBJ ID]

            [OBJ TYPE] is a required argument that can be any of the following:
                BaseModel, User, State, City, Place, Amenity, Review.
            [OBJ ID] is a required argument and is the object's ID, which can
                be accessed via <instance name>.id.
        '''
        args = list(filter(None, line.split(' ')))
        if len(args) == 0:
            print('** class name missing **')
        elif len(args) >= 1:
            try:
                _ = eval(args[0])()
                del models.storage._FileStorage__objects[_.__class__.__name__ +
                                                         '.' + _.id]
                models.storage.save()
            except NameError:
                print("** class doesn't exist **")
                return
            try:
                if args[0] + '.' + args[1] not in \
                 models.storage._FileStorage__objects:
                    print('** no instance found **')
                    return
                else:
                    del models.storage._FileStorage__objects[args[0] + '.' +
                                                             args[1]]
                    models.storage.save()
            except IndexError:
                print('** instance id missing **')
                return

    def do_all(self, line):
        ''' Print string representations of all instances.

            USAGE: all <OBJ TYPE>

            <OBJ TYPE> is an optional argument that, when provided, will only
                print the string representations of objects of that type. It
                can be any of the following: BaseModel, User, State, City,
                Place, Amenity, Review.
        '''
        lst = []
        if line != '':
            args = line.split(' ')
            try:
                var = eval(args[0])()
                var_key = var.__class__.__name__ + '.' + var.id
                del models.storage._FileStorage__objects[var_key]
                models.storage.save()
            except NameError:
                print("** class doesn't exist **")
                return
        for identity, obj in models.storage._FileStorage__objects.items():
            if line == '':
                lst.append(str(obj))
            else:
                if args[0] == obj.__class__.__name__:
                    lst.append(str(obj))
        print(lst)

    def do_update(self, line):
        ''' Update instance attribute and save changes to JSON file.

            USAGE: update [OBJ TYPE] [OBJ ID] [ATTR NAME] [VALUE]

            [OBJ TYPE] is a required argument that can be any of the following:
                BaseModel, User, State, City, Place, Amenity, Review.
            [OBJ ID] is a required argument that is the object's ID, which can
                be accessed via <instance name>.id.
            [ATTR NAME] is the object attribute to add/change.
            [VALUE] is the value to assign to the attribute.
        '''
        if line == '':
            print("** class name missing **")
        else:
            args = line.split(' ')
            try:
                var = eval(args[0])()
                var_key = var.__class__.__name__ + '.' + var.id
                del models.storage._FileStorage__objects[var_key]
                models.storage.save()
            except NameError:
                print("** class doesn't exist **")
                return
            try:
                args[1]
            except IndexError:
                print("** instance id missing **")
                return
            try:
                models.storage._FileStorage__objects[args[0] + '.' + args[1]]
            except KeyError:
                print("** no instance found **")
                return
            try:
                args[2]
            except IndexError:
                print("** attribute name missing **")
                return
            try:
                args[3]
            except IndexError:
                print("** value missing **")
                return
            args[3] = args[3][1:-1]
            if args[0] + '.' + args[1] in models.storage._FileStorage__objects:
                obj = models.storage._FileStorage__objects[args[0] + '.' +
                                                           args[1]]
                setattr(obj, args[2], args[3])
                models.storage.save()

    def default(self, line):
        ''' Overwrite default method. '''
        first_line = line.split(',')
        elements = line.split('.')
        args = elements[1].split('(')
        # new_line = elements[1][elements[1].find("(")+1:elements[1].find(")")]
        if args[0] == 'all':
            HBNBCommand.do_all(self, elements[0])
        elif args[0] == 'count':
            count = 0
            for obj in models.storage._FileStorage__objects.values():
                if elements[0] == obj.__class__.__name__:
                    count += 1
            print(count)
        elif args[0] == 'show':
            line = elements[0] + ' ' + args[1][1:-2]
            HBNBCommand.do_show(self, line)
        elif args[0] == 'destroy':
            line = elements[0] + ' ' + args[1][1:-2]
            HBNBCommand.do_destroy(self, line)
        elif args[0] == 'update':
            args[1] = args[1][:-1]
            params = args[1].split(', ')
            line = elements[0]
            for p in range(len(params)):
                if p != 2:
                    params[p] = params[p][1:-1]
                line = line + ' ' + params[p]
            print(line)
            HBNBCommand.do_update(self, line)
        else:
            pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
