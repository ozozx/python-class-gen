import os
import sys

OUTPRINT = True

def camelize(string):
	words = string.split(' ')
	for i, w in enumerate(words):
		words[i] = w.capitalize()
	return ''.join(words)

def digest_args():
	is_name = True
	args_dict = {}
	hide = False
	props_list = []
	method_list = []
	inherit_list = []
	for arg in sys.argv[1:]:
		if arg[:1] == '-':
			if arg[1:9] == 'inherit:':
				inherit_list.append([arg[9:],'',[]])
			elif arg[1:] == 'hide':
				hide = True
			elif arg[1:] == 'show':
				hide = False
			elif arg[1:] == 'abstract':
				args_dict['abstract'] = True
			else:
				raise Exception("INVALID MODIFIER")
		else:
			if is_name:
				args_dict["name"] = arg
			else:
				if arg.lower()[-2:] == '()':
					method_list.append(arg.lower()[:-2])
				else:
					props_list.append((arg.lower(),hide))
			is_name = False
	if len(inherit_list) > 0:
		args_dict['inherit'] = inherit_list
		# args_dict['abstract'] = False
	if len(props_list) > 0:
		args_dict["props"] = props_list
		if not "abstract" in args_dict.keys():
			args_dict['abstract'] = False
	if "inherit" in args_dict.keys() and args_dict['abstract']:
		raise Exception("ABSTRACT CAN ONLY BE BASE CLASS")
	return args_dict

def dissect_parent(source):
	if os.path.isfile(os.path.join(os.getcwd(), f"{source[0].lower().replace(' ', '_')}.py")):
		f = open(os.path.join(os.getcwd(), f"{source[0].lower().replace(' ', '_')}.py"), "r")
		for l in f.readlines():
			if 'def __init__(self, ' in l:
				inherit_args = l[l.find('def __init__(self, ') + len('def __init__(self, '):-3]
				break
		f.close()

def pull_args():
	class_args = digest_args()
	if not "name" in class_args.keys():
		class_args["name"] = input("Enter Class name (lowercase with spaces if needed): ")
	if (not "inherit" in class_args.keys()) and (not "props" in class_args.keys()) and (not ("abstract" in class_args.keys() and class_args["abstract"])):
		if not "abstract" in class_args.keys():
			abs_ask = input("Do you want the class to be an abstract class? answer with ( Y / N ): ")
			while not (abs_ask.lower().strip() == 'y' or abs_ask.lower().strip() == 'n'):
				abs_ask = input("Invalid input, please answer with ( Y / N ): ")
			if abs_ask.lower().strip() == 'y':
				class_args["abstract"] = True
			else:
				class_args["abstract"] = False
		if not class_args['abstract']:
			print("Do you want the class to inherit from a different class? Custom classes must be in the same directory.")
			parent_ask = input("press Enter without typing to skip: ")
			while not parent_ask == '':
				class_args["inherit"].append([parent_ask,'',[]])
				parent_ask = input("Keep typing for more inheritance,\npress Enter without typing to stop: ")
	if not "props" in class_args.keys():
		print("Start naming properties for the class, properties are visible by default.\nWrite '-hide' to hide properties going forward and add getters and setters for access,\nwrite '-show' to make them visible again.")
		hide = False
		while True:
			prop = input(f"Enter property name (snake_case), press Enter without input to complete.\n{'hidden'*hide}{'visible'*(not hide)} property: ")
			if prop == '' or prop.isspace():
				break
			elif prop[:1] == '-':
				if prop[1:] == 'hide':
					hide = True
				elif prop[1:] == 'show':
					hide = False
				else:
					raise Exception("INVALID MODIFIER")
			else:
				if 'props' in class_args.keys():
					class_args['props'].append((prop.replace(" ","_").lower(),hide))
				else:
					class_args['props'] = [(prop.replace(" ","_").lower(),hide)]
	if 'inherit' in class_args.keys():

	return class_args

def main():
	class_args = pull_args()
	f = open(os.path.join(os.getcwd(), f"{class_args['name'].lower().replace(' ', '_')}.py"), "w")
	print(os.path.join(os.getcwd(),f"{class_args['name'].lower().replace(' ','_')}.py")) if OUTPRINT else print('', end='')
	if 'inherit' in class_args.keys():
		print(f"from {class_args['inherit'].lower().replace(' ','_')} import {camelize(class_args['inherit'])}\n\nclass {camelize(class_args['name'])}({camelize(class_args['inherit'])}):\n") if OUTPRINT else print('', end='')
		f.write(f"from {class_args['inherit'].lower().replace(' ','_')} import {camelize(class_args['inherit'])}\n\nclass {camelize(class_args['name'])}({camelize(class_args['inherit'])}):\n\n")
	else:
		abc_import = 'from abc import *\n\n'
		print(f"{abc_import*class_args['abstract']}class {camelize(class_args['name'])}{'(ABC)'*class_args['abstract']}:") if OUTPRINT else print('', end='')
		f.write(f"{abc_import*class_args['abstract']}class {camelize(class_args['name'])}{'(ABC)'*class_args['abstract']}:\n")
	class_props = []
	if 'props' in class_args.keys():
		for v, k in class_args['props']:
			class_props.append(v)
	abc_import = '\n\t@abstractmethod'
	print(f"{abc_import*class_args['abstract']}\n\tdef __init__(self{', '*(not inherit_args == '')}{inherit_args}{', '*('props' in class_args.keys())}{', '.join(class_props)}):") if OUTPRINT else print('', end='')
	f.write(f"{abc_import*class_args['abstract']}\n\tdef __init__(self{', '*(not inherit_args == '')}{inherit_args}{', '*('props' in class_args.keys())}{', '.join(class_props)}):\n")
	del class_props
	if "inherit" in class_args.keys():
		print(f"\t\tsuper().__init__({inherit_args})") if OUTPRINT else print('', end='')
		f.write(f"\t\tsuper().__init__({inherit_args})\n")
	if 'props' in class_args.keys():
		for p, h in class_args['props']:
			print(f"\t\tself.{'__'*h}{p} = {p}") if OUTPRINT else print('', end='')
			f.write(f"\t\tself.{'__'*h}{p} = {p}\n")
		for p, h in class_args['props']:
			if h:
				print(f"\n\t@property\n\tdef {p}(self):\n\t\treturn self.__{p}\n\n\t@{p}.setter\n\tdef {p}(self, {p}):\n\t\tself.__{p} = {p}") if OUTPRINT else print('', end='')
				f.write(f"\n\t@property\n\tdef {p}(self):\n\t\treturn self.__{p}\n\n\t@{p}.setter\n\tdef {p}(self, {p}):\n\t\tself.__{p} = {p}\n")
	f.close()

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(f"{type(e).__name__} {str(e)}")
	input('Press Enter to close.') if OUTPRINT else print('', end='')