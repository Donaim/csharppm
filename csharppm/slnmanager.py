import random, os
from props import *
from slnparser import *
from os import path
import pmanager as pm

class slnmng(cssln):
    def __init__(self, file):
        self.slnfile = file
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
            loc = pjoin(slndir, p.path)
            proj = pm.csproj(loc)
            self.projects.append( proj )

    def create_reference(self, project_name, reference_source_dll):
        if not path.isfile(reference_source_dll): raise Exception("Source dll ({}) does not exist!".format(reference_source_dll))
        copy_dir_files(path.dirname(reference_source_dll), pjoin(slndir, 'ref')) # copy references to local 'ref' folder
        reference_path = pjoin(slndir, 'ref', path.basename(reference_source_dll))
        self.add_reference(project_name, reference_path=reference_path, reference_source_dll=reference_source_dll)
    def add_reference(self, project_name, reference_path, reference_source_dll):
        proj = self.__get_project_by_name(project_name)
        proj.add_reference(reference_path, None, SourcePath=reference_source_dll)
        proj.save()
    def update_references(self):
        raise NotImplementedError()
    def list_proj_references(self, project_name):
        proj = self.__get_project_by_name(project_name)
        print(proj.get_references())

    def create_project(self, file, type = slndata.csharpstdtype, fver = slndata.csharpstdver):
        guid = pm.csproject_creator.get_guid()
        name = path.basename(file).split('.')[0]

        pm.csproject_creator.create(file, pm.csproj_props(name=name, fver=fver, type=type, guid=guid))
        self.projects.append( pm.csproj(file) )
        self.add_new_project( slnProjInfo(name, file, guid, slndata.csharpguid) )
        self.save()


    def __get_project_by_name(self, name):
        for h in self.projects:
            if(h.name == name): return h

        raise Exception("Wrong project name: \"{}\"".format(name))
    def get_project_names(self):
        return list(map(lambda p: p.name, self.projects))

    def save(self):
        write_file(self.slnfile, str(self))


