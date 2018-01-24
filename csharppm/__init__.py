#! /usr/bin/python3

# import test
# import entry
import props
import sys, os
import props, slndata
import argparse
import slnmanager

class helper:
    def get_sln_file():
        for f in os.listdir(props.slndir):
            if(f.endswith('.sln')):
                return os.path.join(props.slndir, f)
        return props.pjoin(props.slndir, os.path.basename(props.slndir) + '.sln')

class MParser(object):
    def __init__(self):
        self.get_objects()

        self.parser = argparse.ArgumentParser(description='C# project manager', usage=slndata.stript_usage_info)
        self.parse_command()
        
    def parse_command(self):
        self.parser.add_argument('command', help='Subcommand to run')
        args = self.parser.parse_args(sys.argv[2:3])
        for k, v in self.sln_actions.items():
            if(k == args.command): 
                v()
                return
        for p in self.projects:
            if(p == args.command):
                self.parse_project(p)
                return
        
        raise Exception("Wrong command \"{}\" expected to be: [{}]".format(args.command, self.projects + list(self.sln_actions.keys())))

    def parse_project(self, project_name):
        print("Parsing {} project ".format(project_name))

    def get_objects(self):
        self.sln_file = helper.get_sln_file()
        self.sln_name = os.path.basename(self.sln_file).split('.')[0]

        self.sln_actions = {
            'addproj': self.add_proj, 
            'backup': self.backup}
        
        self.sln_mgr = slnmanager.slnmng(self.sln_file)
        self.projects = self.sln_mgr.get_project_names()
        

    def backup(self):
        print("backing up {} ".format(self.sln_name))
    def add_proj(self):
        print("adding project to {}".format(self.sln_name))

    def commit(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print('Running git commit, amend=%s' % args.amend)

    def fetch(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])
        print('Running git fetch, repository=%s' % args.repository)


if __name__ == "__main__":
    MParser()