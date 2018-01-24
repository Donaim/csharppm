#! /usr/bin/python3

# import test
# import entry
import props
import sys, os, shutil
import props, slndata
import argparse
import slnmanager

# print(sys.argv)

class helper:
    def get_sln_file():
        for f in os.listdir(props.slndir):
            if(f.endswith('.sln')):
                return os.path.join(props.slndir, f)
        return None

class MParser(object):
    def __init__(self):
        self.get_objects()

        self.parse_command()
        
    def parse_command(self):
        parser = argparse.ArgumentParser(description='C# project manager', usage=slndata.stript_usage_info)
        parser.add_argument('command', help='Solution command {} or project name {}'.format(list(self.sln_actions.keys()), self.get_project_names()))
        args = parser.parse_args(sys.argv[1:2])
        for k, v in self.sln_actions.items():
            if(k == args.command): 
                v()
                return
        for p in self.get_project_names():
            if(p == args.command):
                self.parse_project(p)
                return
        
        raise Exception("Wrong command \"{}\" expected to be: {}".format(args.command, self.get_project_names() + list(self.sln_actions.keys())))

    def get_project_names(self):
        if(self.sln_file != None):
            return self.sln_mgr.get_project_names()
        else: return []
    def parse_project(self, project_name):
        print("Parsing {} project ".format(project_name))

    def get_objects(self):
        self.sln_file = helper.get_sln_file()
        self.init_solution()
        
        self.sln_actions = {
            'init' : self.init_solution,
            'addproj': self.add_proj, 
            'backup': self.backup}

    def init_solution(self): 
        if self.sln_file == None: 
            self.sln_file = props.pjoin(props.slndir, os.path.basename(props.slndir) + '.sln') # creates new solution file
        self.sln_name = os.path.basename(self.sln_file).split('.')[0]
        self.sln_mgr = slnmanager.slnmng(self.sln_file)
    
    def backup(self):
        shutil.copytree(props.slndir, props.slndir + '.backup')
        print("{} was backed up successfuly".format(self.sln_name))

    def add_proj(self):
        if(self.sln_file == None): 
            self.init_solution()
            # raise Exception("Create solution first with \"{} init\"".format(props.script_name))
        
        parser = argparse.ArgumentParser(description='Gets project arguments')
        parser.add_argument('file')
        parser.add_argument('--type', default=slndata.csharpstdtype)
        parser.add_argument('--fver', default=slndata.csharpstdver)

        args = parser.parse_args(sys.argv[2:])
        if ('/' not in args.file) and ('\\' not in args.file): # mean we entered only a name of project, not path
            args.file = props.pjoin(args.file, args.file + '.csproj')   

        self.sln_mgr.create_project(args.file, args.type, args.fver)
        print("Project {} added to {} solution".format(args.file, self.sln_name))


if __name__ == "__main__":
    MParser()