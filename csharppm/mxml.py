
from lxml import etree # http://lxml.de/installation.html
import props

def find_all_0tag(curr, name):
    re = []
    for c in curr:
        if(etree.QName(c).localname == name): return re.append(c)
    return re
def find_0tag(curr, name):
    for c in curr:
        if(etree.QName(c).localname == name): return c
    return None
def find_tag(curr, name): # only first occurence returned | None
    if(etree.QName(curr).localname == name): return curr
    else:
        for c in curr:
            f = find_tag(c, name)
            if f != None: return f
        return None
def find_all_tags(root, name): # returned all occurences list | []
    re = []
    def find_local(curr):
        if(etree.QName(curr).localname == name): re.append(curr)
        for c in curr: find_local(c)
    find_local(root)
    return re
def rename_tree(tree, newtag):
    nspace = etree.QName(tree).namespace
    if nspace != None and len(nspace) > 0:
        tree.tag = '{' +   + '}' + newtag
    else:
        tree.tag = newtag

def read_xml_tree(file):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(file, parser)


def write_xml(file, tree, pretty=True):
    et = etree.ElementTree(tree)
    et.write(file, pretty_print=pretty, xml_declaration=True, encoding='UTF-8')

def print_dict(tree):
    print(etree.tostring(tree, pretty_print=True, method="xml", xml_declaration=False))

def cheader(name, **fields):
    ff = {}
    for k, v in fields.items():
        ff['@' + k] = v
    return {name: ff}