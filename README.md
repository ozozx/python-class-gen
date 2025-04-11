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
generate_class.py <class name> [-inherit:<parent class> / -abstract] [-show / -hide] <property1> [-show / -hide] [<property2>]...
```

All properties are shown by default, and therefore have no getters / setters, all properties that are following a `-hide` modifier will be hidden and will have getters / setters until the next `-show` modifier.<br>
The `-inherit:` modifier allows for one parent class to be specified. if the parent class file is present in the current working directory, the program will pull its properties automatically and send it to the `super()` constructor.

Set the constant `OUTPRINT` within the script to `False` to not preview the class.
## Example 1:
the following command:
```commandline
generate_class.py a -abstract prop_1 prop_2 -hide prop_3
```
will generate a file in `.\a.py` with the following contents:
```python
from abc import *

class A(ABC):

	@abstractmethod
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
## Example 2:
This example showcases multiple inheritance:<br>
We'll create ClassA with the following command:
```commandline
generate_class.py class_a -abstract prop_1 -hide prop_2
```
The resulting class is an abstract with 2 properties, 1 hidden:
```python
from abc import *

class ClassA(ABC):


        @abstractmethod
        def __init__(self, prop_1, prop_2):
                self.prop_1 = prop_1
                self.__prop_2 = prop_2

        @property
        def prop_2(self):
                return self.__prop_2

        @prop_2.setter
        def prop_2(self, prop_2):
                self.__prop_2 = prop_2
```
Next we'll create an interface, by making an abstract class and a method, declared with `()` in the end.
```commandline
generate_class.py interface_a -abstract doin_something()
```
```python
from abc import *

class InterfaceA(ABC):


        @abstractmethod
        def doin_something(self):
                pass
```
ClassB will inherit both ClassA and InterfaceA, while still being abstract:
```commandline
generate_class.py class_b -abstract -inherit:class_a -inherit:interface_a prop_3
```
```python
from abc import *
from class_a import ClassA
from interface_a import InterfaceA

class ClassB(ClassA, InterfaceA, ABC):


        @abstractmethod
        def __init__(self, prop_1, prop_2, prop_3):
                ClassA.__init__(self, prop_1, prop_2)
                InterfaceA.__init__(self)
                self.prop_3 = prop_3

        @abstractmethod
        def doin_something(self):
                pass
```
ClassC is also abstract and independent of the others, it contains prop_2 as well:
```commandline
generate_class.py class_c -abstract prop_2 doin_another_thing()
```
```python
from abc import *

class ClassC(ABC):


        @abstractmethod
        def __init__(self, prop_2):
                self.prop_2 = prop_2

        @abstractmethod
        def doin_another_thing(self):
                pass
```
Finally, ClassD can inherit from both ClassB and ClassC, while resolving for the duplicate property how we choose:<br>
Here's what would happen if we used `-merge`:
```commandline
generate_class.py class_d -inherit:class_b -inherit:class_c -merge
```
```python
from typing_extensions import override
from class_b import ClassB
from class_c import ClassC

class ClassD(ClassB, ClassC):


        def __init__(self, prop_1, prop_2, prop_3):
                ClassB.__init__(self, prop_1, prop_2, prop_3)
                ClassC.__init__(self, prop_2)

        @override
        def doin_something(self):
                return ClassB.doin_something(self)

        @override
        def doin_another_thing(self):
                return ClassC.doin_another_thing(self)
```
The same command with the `-split` modifier instead will change the property names to allow for individual values per-constructor.
```commandline
generate_class.py class_d -inherit:class_b -inherit:class_c -split
```
```python
from typing_extensions import override
from class_b import ClassB
from class_c import ClassC

class ClassD(ClassB, ClassC):


        def __init__(self, prop_1, class_b_prop_2, prop_3, class_c_prop_2):
                ClassB.__init__(self, prop_1, class_b_prop_2, prop_3)
                ClassC.__init__(self, class_c_prop_2)

        @override
        def doin_something(self):
                return ClassB.doin_something(self)

        @override
        def doin_another_thing(self):
                return ClassC.doin_another_thing(self)
```
#### Note:
the override import will change depending on the python version:<br>
=>3.12: `from typing import overrides`<br>
=<3.11: `from typing_extensions import override`