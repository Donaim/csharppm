import random, os
from props import *
from slnparser import *
from os import path
import pmanager as pm

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
        self.save()
    def __load_sln(self):
        for p in self.get_headers():
            loc = pjoin(self.cwd, p.path)
            proj = pm.csproj(loc)
            self.projects.append( proj )

    def create_project(self, file, refs = None, type = slndata.csharpstdtype, fver = slndata.csharpstdver):
        guid = pm.csproject_creator.get_guid()
        name = path.basename(file).split('.')[0]

        self.add_new_project( slnProjInfo(name, file, guid, slndata.csharpguid) )
        self.save()

        pm.csproject_creator.create(file, pm.csproj_props(name=name, refs=refs, fver=fver, type=type, guid=guid))

    def save(self):
        write_file(self.slnfile, str(self))


