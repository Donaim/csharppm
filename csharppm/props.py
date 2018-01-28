
import inspect, os, shutil

script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
slndir = os.getcwd()
script_name = 'cspm'

def pjoin(*args):
    re = ""
    for p in args:
        re = os.path.join(re, p)
    return re.replace('\\', os.sep).replace(os.sep + os.sep, os.sep)
def file_extension(path):
    name = os.path.basename(path)
    split = name.split('.')
    if len(split) == 1: return ""
    else: return split[-1]

def read_file(file):
    with open(file, 'r') as f:
        return f.read()
def write_file(file, text):
    def write():
        with open(file, 'w+') as f:
            f.write(text)
    try:
        write()
    except:
        os.mkdir(os.path.dirname(file))
        write()
        pass

def copy_file(source, destination):
    if not os.path.isdir(os.path.dirname(destination)): os.mkdir(os.path.dirname(destination))
    shutil.copy(source, destination)

def copy_dir_files(source, destination):
    if not os.path.isdir(destination): os.mkdir(destination)
    for f in os.listdir(source):
        copy_file(os.path.join(source, f), destination)