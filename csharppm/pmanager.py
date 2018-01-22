import mxml
import json
import os
from collections import OrderedDict


class project:
    def __init__(self, file):
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
        re = self.dict
        for i in path[0:-1]:
            re = re[i]
        re[path[-1]].append(val)

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
        
    def add_reference(self, path, name=None):
        if(name == None):
            name = os.path.basename(path).split(sep='.')[0]
        self.add_field({"@Include": name, "HintPath": path }, 'Project', 'ItemGroup', self.ref_group_index, 'Reference')


