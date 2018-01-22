import random, os
import props
from slnparser import cssln
from pmanager import csproj
from os import path

class slnmng(cssln):
    def __init__(self, file):
        self.slnfile = file
        self.cwd = path.dirname(self.slnfile)
        self.projects = []

        if(path.isfile(self.slnfile)):
            cssln.__init__(self, self.slnfile)
        else:
            cssln.__init__(self, None)
            self.__create_sln()
    def __create_sln(self):
        props.write_file(self.slnfile, str(self))
    def __load_sln(self):
        for p in self.get_headers():
            self.projects.append( csproj(p.path) )
            print(self.projects[-1].name)

    def create_project(self, name, type="Library"):
        pass

