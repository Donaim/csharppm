
import inspect, os
script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def pjoin(*args):
    re = ""
    for p in args:
        re = os.path.join(re, p)
    return re.replace('\\', os.sep).replace(os.sep + os.sep, os.sep)

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
