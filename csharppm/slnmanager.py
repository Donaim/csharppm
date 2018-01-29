import random, os, shutil
from props import *
from slnparser import *
from os import path
import pmanager as pm
from lxml import etree
import mxml

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
            if not proj.ok:
                print("Project {} (at \"{}\") filed to load".format(proj.name, loc))

    def create_reference(self, project_name, reference_source_dll):
        self.__update_ref(reference_source_dll)
        reference_path = pjoin(slndir, 'ref', path.basename(reference_source_dll))
        self.add_reference(project_name, reference_path=reference_path, reference_source_dll=reference_source_dll)
    def add_reference(self, project_name, reference_path, reference_source_dll):
        proj = self.__get_project_by_name(project_name)
        proj.add_reference(reference_path, None, SourcePath=reference_source_dll)
        proj.save()
    def add_reference_to_proj(self, project_name, destination_project_path):
        proj = self.__get_project_by_name(project_name)
        proj.add_reference_to_proj(destination_project_path)
        proj.save()
    def add_system_reference(self, project_name, reference_name):
        proj = self.__get_project_by_name(project_name)
        proj.add_system_reference(reference_name)
        proj.save()
    def __update_ref(self, source_dll):
        if not path.isfile(source_dll): raise Exception("Source dll ({}) does not exist!".format(source_dll))
        copy_dir_files(path.dirname(source_dll), pjoin(slndir, 'ref')) # copy references to local 'ref' folder
    def update_references(self):
        for proj in self.projects:
            for r in proj.get_references():
                sourceEl = mxml.find_0tag(r, 'SourcePath')
                if sourceEl != None: 
                    sourcepath = sourceEl.text
                    self.__update_ref(sourcepath)
    def list_proj_references(self, project_name):
        proj = self.__get_project_by_name(project_name)
        for r in proj.get_references():
            hintEl = mxml.find_0tag(r, 'HintPath')
            hintpath = "?"
            if hintEl != None: hintpath = hintEl.text
            sourceEl = mxml.find_0tag(r, 'SourcePath')
            sourcepath = "Unknown source"
            if sourceEl != None: sourcepath = sourceEl.text
            print("{} {} = \"{}\" [{}]".format(etree.QName(r).localname, r.get("Include") , hintpath, sourcepath))
        for r in mxml.find_all_tags(proj.root, 'ProjectReference'):
            print("{} {}".format(etree.QName(r).localname, r.get("Include")))
    def show_proj_info(self, project_name):
        proj = self.__get_project_by_name(project_name)
        for k, v in vars(proj.get_props()).items():
            print("{}: {}".format(k, v))


    def create_project(self, file, type = slndata.csharpstdtype, fver = slndata.csharpstdver):
        guid = pm.csproject_creator.get_guid()
        name = path.basename(file).split('.')[0]

        pm.csproject_creator.create(file, pm.csproj_props(name=name, fver=fver, type=type, guid=guid))
        self.projects.append( pm.csproj(file) )
        self.add_new_project( slnProjInfo(name, file, guid, slndata.csharpguid) )
        self.save()
    def remove_project(self, project_name, delete_directory):
        proj = self.__get_project_by_name(project_name)
        self.projects.remove(proj)
        for h in self.headers:
            if h.name == project_name: 
                self.headers.remove(h)
                break
        self.save()
        print("Project ({}) was removed from slnfile successfuly".format(project_name))

        if delete_directory:
            self.__delete_project_directory(path.dirname(proj.file))
    def __delete_project_directory(self, dir_path):
        shutil.rmtree(dir_path)
        print("Project directory ({}) was removed successfuly".format(dir_path))

    def __get_project_by_name(self, name):
        for h in self.projects:
            if(h.name == name): return h

        raise Exception("Wrong project name: \"{}\"".format(name))
    def get_project_names(self):
        return list(map(lambda p: p.name, self.projects))

    def save(self):
        write_file(self.slnfile, str(self))


