import os, inspect, random, string
from collections import OrderedDict
import json
import mxml
import props

class project:
    def __init__(self, file):
        self.name = "".join(os.path.basename(file).split('.')[:-1])
        self.file = file
        self.dict = mxml.read_xml(self.file)

    def save(self):
        mxml.write_xml(self.file, self.dict, pretty=True)
    def print(self):
        print(mxml.print_dict(self.dict))
    def print(self, *path):
        print(self.__getp(path))

    def __get(self, path):
        re = self.dict
        for i in path:
            re = re[i]
        return re
    def get(self, *path):
        return self.__get(path)
    def getp(self, *path):
        return self.__getp(path)
    def __getp(self, path):
        re = self.__get(path)
        return json.dumps(re, sort_keys=True, indent=4)
    
    def __set(self, val, path):
        re = self.dict
        for i in path[0:-1]:
            re = re[i]
        re[path[-1]] = val
    def set(self, val, *path):
        self.__set(val, path)

    def add_field(self, val, *path):
        self.__add_field(val, path)
    def __add_field(self, val, path):
        self.__get(path).append(val)

class csproj(project):
    def __init__(self, file):
        project.__init__(self, file)
        self.ref_group_index = self.__get_ref_group()
        self.__check_refrence_format()

    def get_ref_group_index(self): self.ref_group_index
    def __get_ref_group(self):
        lst = self.get('Project', 'ItemGroup')
        for i in range(len(lst)):
            if(type(lst[i]) != type(OrderedDict())): continue
            if('Reference' in lst[i].keys()): return i
        
        lst.append(OrderedDict({'Reference': list()}))
        return len(lst) - 1

    def __check_refrence_format(self):
        if(type(self.get('Project', 'ItemGroup', self.ref_group_index, 'Reference')) != type(list())):
            self.set(list(), 'Project', 'ItemGroup', self.ref_group_index, 'Reference')
        
    def add_reference(self, path, name=None, SourcePath=None):
        if(name == None):
            name = os.path.basename(path).split(sep='.')[0]

        path = os.path.relpath(path, os.path.dirname(self.file)).replace('/', '\\') # canonical styling

        field = {"@Include": name, "HintPath": path }
        if SourcePath != None:
            field['SourcePath'] = SourcePath

        self.add_field(field, 'Project', 'ItemGroup', self.ref_group_index, 'Reference')

class csproj_props:
    def __init__(self, name, fver, type, guid):
        self.name = name
        self.fver = fver
        self.type = type
        self.guid = guid

class csproject_creator:
    def create(file, pr):
        text = csproject_creator.generate(pr)
        props.write_file(file, text)

    def generate(pr):
        re = csproject_creator.read_template()

        re = re.replace("#name#", pr.name)
        re = re.replace("#fver#", pr.fver)
        re = re.replace("#type#", pr.type)
        re = re.replace("#guid#", pr.guid)
        return re

    def read_template():
        return props.read_file(props.pjoin( props.script_dir, 'template.csproj' ))

    def get_guid():
        hex = string.digits + "ABCDEF"
        def rand_hex(len):
            lst = [random.choice(hex) for n in range(len)]
            return "".join(lst)
        return '{' + rand_hex(8) + '-' + rand_hex(4) + '-' + rand_hex(4) + '-' + rand_hex(4) + '-' + rand_hex(12) + '}'

