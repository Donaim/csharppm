
import inspect, os
script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def read_file(file):
    with open(file, 'r') as f:
        return f.read()
def write_file(file, text):
    with open(file, 'w+') as f:
        f.write(text)
