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
        self.sln_actions = {
            'init' : self.init_solution,
            'addproj': self.add_proj, 
            'backup': self.backup,
            'updateref': self.update_references,
            }
        
        parser = argparse.ArgumentParser(usage=slndata.stript_usage_info)
        parser.add_argument('command', help='Solution command {} or project name {}'.format(list(self.sln_actions.keys()), self.get_project_names()))
        args = parser.parse_args(sys.argv[1:2])

        for k, v in self.sln_actions.items():
            if(k == args.command): 
                v()
                return
        for p in self.get_project_names():
            if(p == args.command):
                self.current_project = p
                self.parse_project()
                return
        
        raise Exception("Wrong command \"{}\" expected to be: {}".format(args.command, self.get_project_names() + list(self.sln_actions.keys())))

    def get_project_names(self):
        if(self.sln_file != None):
            return self.sln_mgr.get_project_names()
        else: return []

    def get_objects(self):
        self.sln_file = helper.get_sln_file()
        self.init_solution()

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
        
        parser = argparse.ArgumentParser(description='Gets add project arguments')
        parser.add_argument('file')
        parser.add_argument('--type', default=slndata.csharpstdtype)
        parser.add_argument('--fver', default=slndata.csharpstdver)

        args = parser.parse_args(sys.argv[2:])
        if ('/' not in args.file) and ('\\' not in args.file): # means we entered only a name of project, not path
            args.file = props.pjoin(args.file, args.file + '.csproj')   

        self.sln_mgr.create_project(args.file, args.type, args.fver)
        print("Project {} added to {} solution".format(args.file, self.sln_name))
    def update_references():
        raise NotImplementedError()

    def parse_project(self):
        self.project_actions = {
            'addref' : self.project_add_reference,
            'listref' : self.list_proj_references,
            }

        usage = ('{} {} proj_command:{}'.format(props.script_name, self.current_project, list(self.project_actions.keys()))).replace('[', '{').replace(']', '}').replace('\'', "")
        parser = argparse.ArgumentParser(description='Project subparser', usage=usage)
        parser.add_argument('proj_command', help='Project command {} '.format(list(self.sln_actions.keys())))
        args = parser.parse_args(sys.argv[2:3])
        
        for k, v in self.project_actions.items():
            if(k == args.proj_command): 
                v()
                return
        
        raise Exception("Wrong proj_command \"{}\" expected to be: {}".format(args.proj_command, list(self.project_actions.keys())))

    def project_add_reference(self):
        parser = argparse.ArgumentParser(description='Gets add reference arguments', usage='{} {} addref fullpath'.format(props.script_name, self.current_project))
        parser.add_argument('fullpath', help='Path to source dll (gonna be copied to \"\\ref\" folder)')

        args = parser.parse_args(sys.argv[3:])

        self.sln_mgr.create_reference(self.current_project, args.fullpath)

        print("Reference \"{}\" added to project {} ".format(args.fullpath, self.current_project))
    def list_proj_references(self):
        self.sln_mgr.list_proj_references(self.current_project)

if __name__ == "__main__":
    MParser()