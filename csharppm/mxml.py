
import xmltodict as xml # https://github.com/martinblech/xmltodict
from lxml import etree # http://lxml.de/installation.html
import json
import props

def find_tag(name, curr): # only first occurence returned | None
    if(curr.tag.endswith(name)): return curr
    else:
        for c in curr:
            f = find_tag(name, c)
            if f != None: return f
        return None
def find_all_tags(name, root): # returned all occurences list | []
    re = []
    def __find_all_tags(curr):
        if(curr.tag.endswith(name)): return re.append(curr)
        else:
            for c in curr:
                f = __find_all_tags(c)
    __find_all_tags(root)
    return re


def read_xml(file):
    text = props.read_file(file)
    return xml.parse(text)
def write_xml(file, dict, pretty=True):
    text = xml.unparse(dict, pretty=pretty)
    props.write_file(file, text)

def print_dict(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))

def cheader(name, **fields):
    ff = {}
    for k, v in fields.items():
        ff['@' + k] = v
    return {name: ff}