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
        self.__check_refrence_format()

    def __check_refrence_format(self):
        if(type(self.get('Project', 'ItemGroup', -1)) != type(OrderedDict())):
            self.set(OrderedDict({'Reference': list()}), 'Project', 'ItemGroup', -1)
        elif(type(self.get('Project', 'ItemGroup', -1, 'Reference')) != type(list())):
            self.set(list(), 'Project', 'ItemGroup', -1, 'Reference')
        
    def add_reference(self, path, name=None):
        if(name == None):
            name = os.path.basename(path).split(sep='.')[0]
        self.add_field({"@Include": name, "HintPath": path }, 'Project', 'ItemGroup', -1, 'Reference')