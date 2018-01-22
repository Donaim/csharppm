import random, os
from props import *
from slnparser import cssln
from pmanager import csproj
from os import path

class slnmng(cssln):
    def __init__(self, file):
        self.slnfile = file
        self.cwd = os.getcwd()
        self.projects = []

        if(path.isfile(self.slnfile)):
            cssln.__init__(self, self.slnfile)
            self.__load_sln()
        else:
            cssln.__init__(self, None)
            self.__create_sln()
    def __create_sln(self):
        props.write_file(self.slnfile, str(self))
    def __load_sln(self):
        for p in self.get_headers():
            loc = pjoin(self.cwd, p.path)
            proj = csproj(loc)
            self.projects.append( proj )

    def create_project(self, name, type="Library"):
        pass

