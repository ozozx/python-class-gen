import os
import sys
import datetime as dt

OUTPRINT = True
DEBUG = False
LOG = False

def strout_pipe(string:str, logf, is_input:bool =False,filter:bool=True,open_file=None):
	opstr = ''
	if filter:
		if is_input:
			opstr = input(string)
		else:
			print(string)
		if LOG:
			tempf = open(logf, 'a')
			tempf.write(f"{string}{opstr}\n")
			tempf.close()
	if not open_file == None:
		open_file.write(f"{string}{opstr}\n")
	return opstr

def camelize(string, logf):
	try:
		strout_pipe('DEBUG: camelize()',logf,True,DEBUG)
		words = string.replace('_',' ').split(' ')
		for i, w in enumerate(words):
			words[i] = w.capitalize()
		return ''.join(words)
	except Exception as e:
		if not str(e) == 'BUSTED':
			strout_pipe("camelize() {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}",logf)
		raise Exception('BUSTED')

def list_unique(array, logf):
	try:
		strout_pipe(f"DEBUG: list_unique({array})",logf,True,DEBUG)
		u_array = array.copy()
		unfinished = True
		while unfinished:
			unfinished = False
			for key, item in enumerate(u_array[::-1]):
				if u_array.count(item)>1:
					unfinished = True
					u_array.pop(len(u_array)-1-key)
		strout_pipe('DEBUG: list_unique(end)',logf,True,DEBUG)
		return u_array
	except Exception as e:
		if not str(e) == 'BUSTED':
			strout_pipe(f"list_unique({array}) {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}",logf)
		raise Exception('BUSTED')

def digest_args(logf):
	try:
		strout_pipe('DEBUG: digest_args()',logf,True,DEBUG)
		is_name = True
		args_dict = {}
		hide = False
		props_list = []
		method_list = []
		inherit_list = []
		for arg in sys.argv[1:]:
			if arg[:1] == '-':
				if arg[1:9] == 'inherit:':
					inherit_list.append(arg[9:])
				elif arg[1:] == 'hide':
					hide = True
				elif arg[1:] == 'show':
					hide = False
				elif arg[1:] == 'abstract':
					args_dict['abstract'] = True
				elif arg[1:] == 'merge' and not 'merge' in args_dict.keys() :
					args_dict['merge'] = True
				elif arg[1:] == 'split' and not 'merge' in args_dict.keys():
					args_dict['merge'] = False
				else:
					raise TypeError("INVALID MODIFIER")
			else:
				if is_name:
					args_dict["name"] = arg
				else:
					if arg.lower()[-2:] == '()':
						method_list.append((arg.lower()[:-2],hide))
					else:
						props_list.append((arg,hide))
				is_name = False
		if len(inherit_list) > 0:
			strout_pipe('DEBUG: digest_args(inherit unique)',logf,True,DEBUG)
			args_dict['inherit'] = []
			for parent in list_unique(inherit_list,logf):
				args_dict['inherit'].append([parent,'',[]])
		strout_pipe('DEBUG: digest_args(prop unique)',logf,True,DEBUG)
		if len(props_list) > 0:
			args_dict["props"] = list_unique(props_list,logf)
		strout_pipe('DEBUG: digest_args(method unique)',logf,True,DEBUG)
		if len(method_list) > 0:
			args_dict["methods"] = list_unique(method_list,logf)
		if (len(props_list) > 0 or len(method_list) > 0) and (not 'abstract' in args_dict.keys()):
			args_dict["abstract"] = False
		strout_pipe('DEBUG: {args_dict}',logf,True,DEBUG)
		strout_pipe('DEBUG: digest_args(end)',logf,True,DEBUG)
		return args_dict
	except Exception as e:
		if not str(e) == 'BUSTED':
			strout_pipe(f"digest_args() {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}",logf)
		raise Exception('BUSTED')

def dissect_parent(source, logf):
	try:
		strout_pipe('DEBUG: dissect_parent()',logf,True,DEBUG)
		if os.path.isfile(os.path.join(os.getcwd(), f"{source[0].lower().replace(' ', '_')}.py")):
			f = open(os.path.join(os.getcwd(), f"{source[0].lower().replace(' ', '_')}.py"), "r")
			lines = f.readlines()
			for ln, l in enumerate(lines):
				if 'def __init__(self, ' in l:
					source[1] = l[l.find('def __init__(self, ') + len('def __init__(self, '):-3]
				elif 'def ' in l and '@abstract' in lines[ln-1]:
					metargs = ''
					if '(self,' in l:
						metargs = l[l.find('(self,')+len('(self,') : l[l.find(')')]].strip()
					source[2].append((l[l.find('def ')+len('def ') : l.find('(self')].strip(),metargs))
			f.close()
		strout_pipe('DEBUG: dissect_parent(end)',logf,True,DEBUG)
	except Exception as e:
		if not str(e) == 'BUSTED':
			strout_pipe(f"dissect_parent() {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}",logf)
		raise Exception('BUSTED')

def pull_args(logf):
	try:
		class_args = digest_args(logf)
		strout_pipe('DEBUG: pull_args()',logf,True,DEBUG)
		if not "name" in class_args.keys():
			class_args["name"] = strout_pipe("Enter Class name (lowercase with spaces if needed): ",logf,True)
		if (not ("props" in class_args.keys() or "methods" in class_args.keys())) and (not ("abstract" in class_args.keys() and class_args["abstract"])):
			if not "abstract" in class_args.keys():
				if not "inherit" in class_args.keys():
					abs_ask = strout_pipe("Do you want the class to be an abstract class? answer with ( Y / N ): ",logf,True)
					while not (abs_ask.lower().strip() == 'y' or abs_ask.lower().strip() == 'n'):
						abs_ask = strout_pipe("Invalid input, please answer with ( Y / N ): ",logf,True)
					if abs_ask.lower().strip() == 'y':
						class_args["abstract"] = True
					else:
						class_args["abstract"] = False
				else:
					class_args["abstract"] = False
			if not "inherit" in class_args.keys():
				strout_pipe("Do you want the class to inherit from a different class? Custom classes must be in the same directory.",logf)
				parent_ask = strout_pipe("press Enter without typing to skip: ",logf,True)
				while not parent_ask == '':
					if 'inherit' in class_args.keys():
						class_args['inherit'].append([parent_ask,'',[]])
					else:
						class_args['inherit'] = [[parent_ask,'',[]]]
					parent_ask = strout_pipe("Keep typing for more inheritance,\npress Enter without typing to stop: ",logf,True)
		if not ("props" in class_args.keys() or "methods" in class_args.keys()):
			strout_pipe("Start naming properties and methods for the class (methods end with '()'), properties are visible by default.\nWrite '-hide' to hide properties going forward and add getters and setters for access,\nwrite '-show' to make them visible again.",logf)
			hide = False
			while True:
				prop = strout_pipe(f"Enter property name (snake_case) or method name (snake_case_with_brackets()), press Enter without input to complete.\n{'hidden'*hide}{'visible'*(not hide)} property/method: ",logf,True)
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
					if prop.lower()[-2:] == '()':
						if not 'methods' in class_args.keys():
							class_args['methods'] = [(prop.replace(" ","_").lower()[:-2],hide)]
						elif (prop.replace(" ","_").lower()[:-2],hide) in class_args['methods'] or (prop.replace(" ","_").lower()[:-2], not hide) in class_args['methods']:
							raise Exception("DUPLICATE METHOD")
						else:
							class_args['methods'].append((prop.replace(" ","_").lower()[:-2],hide))
					else:
						if not 'props' in class_args.keys():
							class_args['props'] = [(prop.replace(" ","_"),hide)]
						elif (prop.replace(" ", "_"), hide) in class_args['props'] or (prop.replace(" ", "_"), not hide) in class_args['props']:
							raise Exception("DUPLICATE PROP")
						else:
							class_args['props'].append((prop.replace(" ","_"),hide))
		if 'inherit' in class_args.keys():
			inherit_args = []
			for parent in class_args['inherit']:
				dissect_parent(parent,logf)
				if not parent[1] == '':
					inherit_args.extend(parent[1].split(', '))
			if len(inherit_args) > len(list_unique(inherit_args,logf)) and not 'merge' in class_args.keys():
				ms_answer = strout_pipe("Multiple arguments of the same name detected in parent classes, do you wish to use the same argument values for all constructors? or split duplicate arguments?\n(merge/split): ",logf,True).lower().strip()
				while not (ms_answer == 'merge' or ms_answer == 'split'):
					ms_answer = strout_pipe("Invalid response, please enter (merge/split): ",logf,True).lower().strip()
				if ms_answer == 'merge':
					class_args['merge'] = True
				else:
					class_args['merge'] = False
		strout_pipe('DEBUG: pull_args(end)',logf,True,DEBUG)
		return class_args
	except Exception as e:
		if not str(e) == 'BUSTED':
			strout_pipe(f"pull_args() {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}",logf)
		raise Exception('BUSTED')

def main(logf):
	try:
		class_args = pull_args(logf)
		strout_pipe('DEBUG: main()',logf,True,DEBUG)
		f = open(os.path.join(os.getcwd(), f"{class_args['name'].lower().replace(' ', '_')}.py"), "w")
		strout_pipe('DEBUG: main(file open)',logf,True,DEBUG)
		strout_pipe(os.path.join(os.getcwd(),f"{class_args['name'].lower().replace(' ','_')}.py"),logf,False,OUTPRINT)
		abc_import = 'from abc import *'
		strout_pipe(f"{abc_import*class_args['abstract']}",logf,False,OUTPRINT,f)
		strout_pipe('DEBUG: main(file abstract?)',logf,True,DEBUG)
		parent_list = []
		enum_flag = False
		strout_pipe('DEBUG: main(if inherit 0)',logf,True,DEBUG)
		if 'inherit' in class_args.keys():
			for parent in class_args['inherit']:
				if parent[0] == 'enum':
					enum_flag = True
				if len(parent[2]) > 0 and not class_args['abstract']:
					strout_pipe(f"from typing{'_extensions'*(sys.version_info[1] < 12)} import override{'s'*(sys.version_info[1] > 11)}",logf,False,OUTPRINT,f)
					break
			for parent in class_args['inherit']:
				strout_pipe(f"from {parent[0].lower().replace(' ','_')} import {camelize(parent[0],logf)}",logf,False,OUTPRINT,f)
				parent_list.append(camelize(parent[0],logf))
		strout_pipe(f"\nclass {camelize(class_args['name'],logf)}{'('*(len(parent_list)>0 or class_args['abstract'])}{', '.join(parent_list)*(len(parent_list)>0)}{', '*(len(parent_list)>0 and class_args['abstract'])}{'ABC'*class_args['abstract']}{')'*(len(parent_list)>0 or class_args['abstract'])}:\n",logf,False,OUTPRINT,f)
		strout_pipe('DEBUG: main(if enum)',logf,True,DEBUG)
		if enum_flag:
			if 'props' in class_args.keys():
				for prop, _ in class_args['props']:
					strout_pipe(f"\t{prop.upper()} = \"{prop.replace('_', ' ')}\"",logf,False,OUTPRINT,f)
			if 'methods' in class_args.keys():
				for method, _ in class_args['methods']:
					strout_pipe(f"\n\t@classmethod\n\tdef {method}(cls)\n\t\tpass",logf,False,OUTPRINT,f)
		else:
			abc_import = '\n\t@abstractmethod'
			inherit_args = ''
			if 'inherit' in class_args.keys():
				for parent in class_args['inherit']:
					if not parent[1] == '':
						inherit_args += ', '+parent[1]
			used_mets = []
			used_props = []
			if (inherit_args == '') and (not 'props' in class_args.keys()):
				if (not "methods" in class_args.keys()):
					strout_pipe("\tpass",logf,False,OUTPRINT,f)
			else:
				if not inherit_args == '':
					dupe_props = inherit_args[2:].split(', ')
					used_props = list_unique(dupe_props,logf)
					if len(dupe_props) > len(used_props):
						if class_args['merge']:
							inherit_args = ', '+', '.join(used_props)
						else:
							for prop in used_props:
								dupe_props.pop(dupe_props.index(prop))
							dupe_props = list_unique(dupe_props,logf)
							inherit_args = ''
							if 'inherit' in class_args.keys():
								used_props = []
								for parent in class_args['inherit']:
									if not parent[1] == '':
										inherit_explode = []
										for prop in parent[1].split(', '):
											inherit_explode.append(f"{(parent[0].lower().replace(' ','_')+'_')*(prop in dupe_props)}{prop}")
										parent[1] = ', '.join(inherit_explode)
										inherit_args += ', '+parent[1]
										used_props.extend(inherit_explode)
				class_props = []
				if 'props' in class_args.keys():
					pop_idxs = []
					idx = 0
					for v, h in class_args['props']:
						if v in used_props:
							pop_idxs.append(idx)
						idx +=1
					for i in pop_idxs[::-1]:
						class_args['props'].pop(i)
					del pop_idxs
					del idx
					for v, h in class_args['props']:
						class_props.append(v.lower().replace(' ','_'))
				strout_pipe(f"{abc_import * class_args['abstract']}\n\tdef __init__(self{inherit_args * (not inherit_args == '')}{', ' * ('props' in class_args.keys())}{', '.join(class_props)}):",logf,False,OUTPRINT,f)
				if "inherit" in class_args.keys():
					if len(class_args['inherit']) == 1:
						strout_pipe(f"\t\tsuper().__init__({class_args['inherit'][0][1]})",logf,False,OUTPRINT,f)
					else:
						for parent in class_args['inherit']:
							strout_pipe(f"\t\t{camelize(parent[0],logf)}.__init__(self{', '*(not parent[1]=='')}{parent[1]})",logf,False,OUTPRINT,f)
				if 'props' in class_args.keys():
					for p, h in class_args['props']:
						strout_pipe(f"\t\tself.{'__'*h}{p.lower().replace(' ','_')} = {p.lower().replace(' ','_')}",logf,False,OUTPRINT,f)
					for p, h in class_args['props']:
						if h:
							strout_pipe(f"\n\t@property\n\tdef {p.lower()}(self):\n\t\treturn self.__{p.lower()}\n\n\t@{p.lower()}.setter\n\tdef {p.lower()}(self, {p.lower()}):\n\t\tself.__{p.lower()} = {p.lower()}",logf,False,OUTPRINT,f)
				if "inherit" in class_args.keys():
					override_txt = '\n\t@override'
					for parent in class_args['inherit']:
						for met_name, met_args in parent[2]:
							if not met_name in used_mets:
								strout_pipe(f"{abc_import*class_args['abstract']}{override_txt*(not class_args['abstract'])}\n\tdef {met_name}(self{met_args}):\n\t\t{'return '*(not class_args['abstract'])}{'super()'*(len(class_args['inherit']) == 1 and not class_args['abstract'])}{camelize(parent[0],logf)*(len(class_args['inherit']) > 1 and not class_args['abstract'])}{'.'*(not class_args['abstract'])}{met_name*(not class_args['abstract'])}{'(self'*(not class_args['abstract'])}{', '*(not (met_args == '' or class_args['abstract']))}{met_args*(not class_args['abstract'])}{')'*(not class_args['abstract'])}{'pass'*class_args['abstract']}",logf,False,OUTPRINT,f)
								used_mets.append(met_name)
			if "methods" in class_args.keys():
				for met_name, hide in class_args['methods']:
					if not met_name in used_mets:
						strout_pipe(f"{abc_import*class_args['abstract']}\n\tdef {'__'*hide}{met_name.lower().replace(' ','_')}(self):\n\t\tpass",logf,False,OUTPRINT,f)
						used_mets.append(met_name)
		f.close()
	except Exception as e:
		if not str(e) == 'BUSTED':
			strout_pipe(f"main() {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}",logf)
		raise Exception('BUSTED')

if __name__ == '__main__':
	log_f = ''
	if LOG:
		log_f = os.path.join(os.getcwd(), dt.datetime.now().strftime("gen_class_%Y_%m_%d_%H_%M_%S.log"))
		tempf = open(log_f,'w')
		tempf.write('WAIT!\n') if DEBUG else print('', end='')
		tempf.close()
	input('WAIT!') if DEBUG else print('', end='')
	try:
		main(log_f)
		strout_pipe('Press Enter to close.',log_f,True,OUTPRINT)
	except Exception as e:
		if not str(e) == 'BUSTED':
			if LOG:
				tempf = open(log_f, 'a')
				tempf.write(f"__main__ {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}\n")
				tempf.close()
			print(f"__main__ {e.__traceback__.tb_lineno}: {type(e).__name__} {str(e)}")
		strout_pipe('Press Enter to close.',logf,True,OUTPRINT)