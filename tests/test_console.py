#!/usr/bin/python3
"""A unittest module for command line intepreter

This test module contain tests for:
    1. if the do_quit() succesfully exit the program
    2. if the do_EOF() succesfully exit the program
    3. if the emptyline() doesn't execute anything
    4. if the do_create() creates a new instance of the Class given
        4a. if the do_create() raises a msg while trying to create
            a class that doesn't exist in the program
        4b. if the do_create() raises a msg when the command is entered
            without any class name
        4c. if the do_create() receives an infinity number as the arg and
            if it sucessfully raise a msg when given infinity number

    5. if the do_show() prints the string representation of an instance
        based on the class name and the id

        5a. if the do_show() raises a msg when it's called alone, without
            a class name
        5b. if the do_show() raises a msg when a class that doesn't exist
            is called along the show command
        5c. if the do_show() raises a msg when a class that exist is only
            passed as the argument but no id
        5d. if the do_show() raises a msg when a class that exist is
            passed along side an id that doesn't exist

    6. if the do_destory() deletes an instance based on the class name and
        id, also save the changes into the Json file

        6a. if the do_destroy() raises a msg when it's called alone,
            without a class name
        6b. if the do_destroy() raises a msg when a class that doesn't
            exist is called along the command
        6c. if the do_destroy() raises a msg when a class that exist is
            only passed as the argument but no id
        6d. if the do_destroy() raises a msg when a class that exist is
            passed along side an id that doesn't exist

    7. if the do_all() prints all string representation of all instances
        based or not on the class name

        7a. if the do_all() prints all instances when the do_all() doesn't
            receive any argument along it
        7b. if the do_all() prints only instances of the class name when
            the do_all() is passed along side a class name
        7c. if the do_all() raises a msg when a class name that doesn't
            exist is passed along side the all() command.

    8. if the do_update() updates an instance based on the class name
        and id by adding or updating attribute

        8a. if the do_update() raises a msg whem there's no argument
            passed along side it's command
        8b. if the do_update() raises a msg when the class name passed
            along side the the do_update() doesn't exist
        8c. if the do_update() raises a msg when a class that exist is
            passed along side the do_update() but the next argument
            after the class name is empty
        8d. if the do_update() raises a msg when a class name that exist
            and an id is passed along the class name, if the id doesn't
            exist but it begins a digit is prints "no instance found"
            if the id doesn't exist but it begins with a string
            it prints "attribute name missing" if the id exist it prints
            "attribute name missing" to indicate it needs an attribute

        8e. if the do_update() raises a msg when the class name exist and
            id exist and the attribute name is not a dict, i.e it has
            no value only key
        8f. if the attribute name passed to the do_update() is in:
            id, created_at, or updated_at, it shouldn't do anything

        8g. A check if the attribute passed to the do_update() has a
        value and it's been added to that particular instance
        8h. A check if the attribute passed to the do_update() has a value
            and it's beiong updated, that means the value only gets
            updated, because the object already contain the key

ALL TESTS WOULD BE TESTED WITH INFINITY AND DIFFERENT TYPES AS ARGUMENTS
ALONGSIDE COMMANDS
"""

from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand
from unittest.mock import patch
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models import storage
from io import StringIO
import unittest
import json
import cmd
import os


class Test_console(unittest.TestCase):
    """Test foundations
        @path('sys.stdout', new_callable=StringIO) is used to capture the
        output printed to the standard output during the execution of each
        command
    """
    # test case if do_quit succesfully exit the program
    def test_quit_command(self):
        console = HBNBCommand()
        with patch("sys.stdout", new=StringIO()) as output:
            with self.assertRaises(SystemExit) as context:
                console.onecmd("EOF")
            self.assertEqual(context.exception.code, 0)

    # test case if do_EOF successfulyy exit the program
    def test_eof_command(self):
        console = HBNBCommand()
        with patch("sys.stdout", new=StringIO()) as output:
            with self.assertRaises(SystemExit) as context:
                console.onecmd("EOF")
            self.assertEqual(context.exception.code, 0)

    def test_help(self):
        h = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(h, output.getvalue().strip())

    # test case if the emptyline() doesn't execute anything
    def test_emptyline_command(self):
        console = HBNBCommand()
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.onecmd(""))
            self.assertEqual("", output.getvalue().strip())

    # test if do_create creates a new instance of allclasses
    @unittest.skipIf(not hasattr(HBNBCommand, 'created_model'), True)
    def test_create_command(self):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        with patch("sys.stdout", new=StringIO()) as output:
            for model_class in classes:
                class_name = model_class.__name__
                self.assertFalse(console.onecmd(f"create {class_name}"))
                created_instance = console.created_model
                self.assertIsInstance(created_instance, model_class)

    # test if do_create raises a msg while trying to create a class that
    # doesn't exist
    def test_create_class_not_exist(self):
        console = HBNBCommand()
        expected = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.onecmd("create MyModel"))
            self.assertEqual(expected, output.getvalue().strip())

    # test if do_create raises a msg when the command is entered
    # without any class name
    def test_create_class_name_missing(self):
        console = HBNBCommand()
        expected = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.onecmd("create"))
            self.assertEqual(expected, output.getvalue().strip())

    # test if the do_show() prints the string representation of an
    # instance based on the class name and the id

    @patch('sys.stdout', new_callable=StringIO)
    @unittest.skipIf(not hasattr(HBNBCommand, 'created_model'), True)
    def test_show_command(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        for model_class in classes:
            class_name = model_class.__name__
            console.do_create(class_name)
            created_id = mock_stdout.getvalue().strip()
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

            # call do_show
            arg = "{} {}".format(class_name, created_id)
            console.do_show(arg)
            dct = console.created_model.__dict__
            expected = "[{}] ({}) {}" .format(class_name, created_id, dct)
            self.assertEqual(mock_stdout.getvalue().strip(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test if the do_show() raises a msg when it's called alone, without
    # a class name
    def test_show_class_name_missing(self):
        console = HBNBCommand()
        expected = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.onecmd("show"))
            self.assertEqual(expected, output.getvalue().strip())

    # test if the do_show() raises a msg when a class that doesn't exist
    # is called along the show command

    def test_show_class_does_not_exist(self):
        console = HBNBCommand()
        expected = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.onecmd(f"show MyModel"))
            self.assertEqual(expected, output.getvalue().strip())

    # test if the do_show() raises a msg when a class that exist is only
    # passed as the argument but no id
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_instance_id_missing(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        expected = "** instance id missing **\n"
        for model_class in classes:
            class_name = model_class.__name__
            created_id = ""
            arg = "{} {}".format(class_name, created_id)
            console.do_show(arg)
            self.assertEqual(mock_stdout.getvalue(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test if the do_show() raises a msg when a class that exist is
    # passed along side an id that doesn't exist

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_no_instance_found(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        expected = "** no instance found **\n"
        for model_class in classes:
            class_name = model_class.__name__
            created_id = "246c227a-d5c1-403d-9bc7-6a47bb9f0f68"
            arg = "{} {}".format(class_name, created_id)
            console.do_show(arg)
            self.assertEqual(mock_stdout.getvalue(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test if the do_destory() deletes an instance based on the class
    # name and id, also save the changes into the Json file

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_destroy(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        for model_class in classes:
            class_name = model_class.__name__
            console.do_create(class_name)
            # get the output from do_create
            created_id = mock_stdout.getvalue().strip()
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

            arg = "{} {}".format(class_name, created_id)

            console.do_destroy(arg)
            instances = storage.all()
            instance_key = "{}.{}".format(class_name, created_id)
            # check if instance is deleted
            self.assertNotIn(instance_key, instances)

            # check if the instamnce is correctly removed from the file
            f_store = FileStorage()
            with open(f_store._FileStorage__file_path, "r") as open_file:
                data = json.load(open_file)
                self.assertNotIn(instance_key, data)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test if the do_destroy() raises a msg when it's called alone
    # without a class name

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_destroy_class_name_missing(self, mock_stdout):
        console = HBNBCommand()
        expected = "** class name missing **\n"
        console.do_destroy("")
        self.assertEqual(mock_stdout.getvalue(), expected)

    # test if the do_destroy() raises a msg when a class that doesn't
    # exist is called along the command

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_destroy_class_does_not_exist(self, mock_stdout):
        console = HBNBCommand()
        expected = "** class doesn't exist **\n"
        classes = ["Hello", None, 3, 3.142, float('inf'), -float('inf'),
                   True, False]
        for model_cls in classes:
            console.do_destroy(str(model_cls))
            self.assertEqual(mock_stdout.getvalue(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test if the do_destroy() raises a msg when a class that exist is
    # only passed as the argument but no id

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_destroy_instance_id_missing(self, mock_stdout):
        console = HBNBCommand()
        expected = "** instance id missing **\n"
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        for model_class in classes:
            class_name = model_class.__name__
            created_id = ""
            arg = "{} {}".format(class_name, created_id)
            console.do_destroy(arg)
            self.assertEqual(mock_stdout.getvalue(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test if the do_destroy() raises a msg when a class that exist is
    # passed along side an id that doesn't exist

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_destroy_no_instance_found(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        expected = "** no instance found **\n"
        for model_class in classes:
            class_name = model_class.__name__
            created_id = "fce12f8a-fdb6-439a-afe8-2881754de71c"
            arg = "{} {}".format(class_name, created_id)
            console.do_destroy(arg)
            self.assertEqual(mock_stdout.getvalue(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

    # test  if the do_all() prints all string representation of all
    # instances based or not on the class name

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all_method(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        for model_class in classes:
            class_name = model_class.__name__
            console.do_create(class_name)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

        # call do_all() without passing any class name to it
        console.do_all("")
        output = mock_stdout.getvalue().strip()
        instances = storage.all()

        for instance in instances.values():
            self.assertIn(str(instance), output)

        mock_stdout.seek(0)
        mock_stdout.truncate(0)

    # test do_all() with class name
    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all_method_with_class_name(self, mock_stdout):
        console = HBNBCommand()
        classes = [BaseModel, User, Place, City, State, Amenity, Review]
        for model_class in classes:
            class_name = model_class.__name__
            console.do_create(class_name)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

        for cls in classes:
            cls_name = cls.__name__
            console.do_all("all " + cls_name)
            output = mock_stdout.getvalue().strip()

            for clas in classes:
                clas_name = clas.__name__
                if clas_name in output:
                    self.assertIn(clas_name, output)
                else:
                    self.assertNotIn(clas_name, output)

    # test if the do_all() raises a msg when a class name that doesn't
    # exist is passed along side the all() command

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all_class_does_not_exist(self, mock_stdout):
        console = HBNBCommand()
        expected = "** class doesn't exist **\n"
        classes = ["Hello", None, 3, 3.142, float('inf'), -float('inf'),
                   True, False]
        for model_cls in classes:
            console.do_all(str(model_cls))
            self.assertEqual(mock_stdout.getvalue(), expected)
            mock_stdout.seek(0)
            mock_stdout.truncate(0)


class TestHBNBCommand_update(unittest.TestCase):
    """do_update() test cases
    """

    # test if do_update() raises a message when no arguments are passed
    def test_do_update_no_arguments(self):
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() raises a message when the class name doesn't exist
    def test_do_update_class_name_missing(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() raises a message when the class name is
    # provided but the next argument is empty
    def test_do_update_missing_id(self):
        expected_output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() raises a message when the instance doesn't
    # exist or the attribute name is missing
    def test_do_update_attribute_missing_digit(self):
        # case when instance doesn't exist (ID starts with a digit)
        expected_output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1234"))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test when instance doesn't exist (ID starts with a string)
    def test_do_update_instance_not_found_string(self):
        # case when instance doesn't exist (ID starts with an alphabet)
        expected_output = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel my_id"))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test when instance exists but attribute name is missing

    def test_do_update_instance_exist_msg(self):
        console = BaseModel()
        i_d = console.id
        expected_output = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel " + i_d))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() raises a message when the attribute value is
    # not a dictionary
    def test_do_update_attribute_value_not_dict(self):
        console = BaseModel()
        my_id = console.id
        expected_output = "** value missing **"
        mod = "update BaseModel "
        att = " some_attribute"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(mod + my_id + att))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() ignores attribute id
    def test_do_update_ignores_reserved_id_attribute(self):
        expected_output = ""
        console = BaseModel()
        my_id = console.id
        mod = "update BaseModel "
        att = " id 1234"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(mod + my_id + att))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() ignores attribute created_at
    def test_do_update_ignores_reserved_created_at_attribute(self):
        expected_output = ""
        console = BaseModel()
        my_id = console.id
        mod = "update BaseModel "
        att = " created_at 2022-01-01T00:00:00"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(mod + my_id + att))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() ignores attribute updated_at
    def test_do_update_ignores_reserved_updated_at_attribute(self):
        expected_output = ""
        console = BaseModel()
        my_id = console.id
        mod = "update BaseModel "
        att = " updated_at 2022-01-01T00:00:00"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(mod + my_id + att))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() correctly adds an attribute to an instance
    def test_do_update_adds_attribute_to_instance(self):
        expected_output = ""
        console = BaseModel()
        my_id = console.id
        mod = "update BaseModel "
        att = " first_name Isaac"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(mod + my_id + att))
            self.assertEqual(expected_output, output.getvalue().strip())

    # test if do_update() correctly updates an attribute of an instance
    def test_do_update_updates_attribute_of_instance(self):
        expected_output = ""
        console = BaseModel()
        my_id = console.id
        mod = "update BaseModel "
        att = " first_name Betty"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(mod + my_id + att))
            self.assertEqual(expected_output, output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for the help message
    """

    def test_help_quit(self):
        h = "Quit is command to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help_create(self):
        h = ("Usage: create <class>\n        "
             "Creates a new class instance and prints it's id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help_EOF(self):
        h = "EOF is command to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help_show(self):
        h = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Prints the string rep of a class given it's class name and id")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help_destroy(self):
        h = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Deletes an instance based on the class name and id")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help_all(self):
        h = ("Usage: all or all <class> or <class>.all()\n        "
             "Prints all string rep of all instances given class or not")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help_update(self):
        h = ("Usage: update <class> <id> <attribute> <value>\n        "
             "Updates an instance based on the class, id, attribute and value")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_count(self):
        h = ("Usage: count <class> or <class>.count()\n        "
             "Prints the number of occurence of a class")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertNotEqual(h, output.getvalue().strip())

    def test_help(self):
        h = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(h, output.getvalue().strip())


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(self):
        exe = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertNotEqual(exe, output.getvalue().strip())

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertNotEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertNotEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertNotEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertNotEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertNotEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertNotEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertNotEqual("1", output.getvalue().strip())


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "User.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "State.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_update_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertNotEqual(correct, output.getvalue().strip())


if __name__ == '__main__':
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        unittest.main()
