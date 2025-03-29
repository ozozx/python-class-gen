# Python Class Generator
A class generator for saving time.<br>
To clone this repository enter the following into your commandline:
```commandline
git clone https://github.com/ozozx/python-class-gen.git
```
## usage:
run the script and follow the prompts, it will generate a class with a full constructor, getters, setters, and singular inheritance.<br>
custom classes need to be in the same directory as the script to pull properties.<br>
does not support automatic method generation, multiple inheritance and overrides.

you can also build the class entirely from the commandline like so:
```commandline
generate_class.py <class name> [-inherit:<parent class>] [-show / -hide] <property1> [-show / -hide] [<property2>]...
```

All properties are shown by default, and therefore have no getters / setters, all properties that are following a `-hide` modifier will be hidden and will have getters / setters until the next `-show` modifier.<br>
The `-inherit:` modifier allows for one parent class to be specified. if the parent class file is present in the current working directory, the program will pull its properties automatically and send it to the `super()` constructor.

Set the constant `OUTPRINT` within the script to `False` to not preview the class.
## Example:
the following command:
```commandline
generate_class.py a prop_1 prop_2 -hide prop_3
```
will generate a file in `.\a.py` with the following contents:
```python
class A:

        def __init__(self, prop_1, prop_2, prop_3):
                self.prop_1 = prop_1
                self.prop_2 = prop_2
                self.__prop_3 = prop_3

        @property
        def prop_3(self):
                return self.__prop_3

        @prop_3.setter
        def prop_3(self, prop_3):
                self.__prop_3 = prop_3
```
after which the following command:
```commandline
generate_class.py b -inherit:a -hide prop_4 -show prop_5
```
will generate a file in `.\b.py` with the following contents:
```python
from a import A
class B(A):

        def __init__(self, prop_1, prop_2, prop_3, prop_4, prop_5):
                super().__init__(prop_1, prop_2, prop_3)
                self.__prop_4 = prop_4
                self.prop_5 = prop_5

        @property
        def prop_4(self):
                return self.__prop_4

        @prop_4.setter
        def prop_4(self, prop_4):
                self.__prop_4 = prop_4
```
after both files are generated, feel free to add methods and overrides manually.