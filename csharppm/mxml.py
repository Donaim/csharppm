
import xmltodict as xml # https://github.com/martinblech/xmltodict
import json
import props

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