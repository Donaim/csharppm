import os, inspect, random, string
from collections import OrderedDict
from lxml import etree # http://lxml.de/installation.html
import props
import mxml

class project:
    def __init__(self, file):
        self.name = "".join(os.path.basename(file).split('.')[:-1])
        self.file = file

        try:
            self.tree = mxml.read_xml_tree(self.file)
            self.root = self.tree.getroot()
            self.ok = True
        except:
            self.tree = None
            self.root = None
            self.ok = False

        if self.ok:
            self.namespace = etree.QName(self.root).namespace
            if self.namespace != None and len(self.namespace) > 0:
                self.namespace = '{' + self.namespace + '}'

    def save(self):
        mxml.write_xml(self.file, self.root)
    def print(self):
        print(mxml.print_dict(self.root))
    def print(self, *path):
        print(self.__getp(path))

    def __get(self, path):
        re = self.root
        for i in path:
            re = mxml.find_0tag(re, i)
            if re == None: return None
        return re
    def get(self, *path):
        return self.__get(path)
    def getp(self, *path):
        return self.__getp(path)
    def __getp(self, path):
        re = self.__get(path)
        return etree.tostring(re, pretty_print=True)
    
    def __set(self, tag, path):
        g = self.__get(path)
        g.text 
    def set(self, val, *path):
        self.__set(val, path)


    def add_field(self, tag, *path):
        return self.__add_field(tag, path)
    def __add_field(self, tag, path):
        return etree.SubElement(self.__get(path), val)

class csproj(project):
    def __init__(self, file):
        project.__init__(self, file)
        self.__check_refrence_format()

    def __check_refrence_format(self):
        pass
    
    def get_props(self):
        name = self.get('PropertyGroup', 'AssemblyName').text
        fver = self.get('PropertyGroup', 'TargetFrameworkVersion').text
        type = mxml.find_tag(self.root, 'OutputType').text
        guid = self.get('PropertyGroup', 'ProjectGuid').text
        return csproj_props(name=name, fver=fver, type=type, guid=guid)

    def get_references(self):
        return mxml.find_all_tags(self.root, 'Reference')
    
    def get_canonical_path(self, path):
        return os.path.relpath(path, os.path.dirname(self.file)).replace('/', '\\') # canonical styling
    def add_reference(self, path, name=None, SourcePath=None):
        if(name == None):
            name = os.path.basename(path).split(sep='.')[0]
        path = self.get_canonical_path(path)

        itemg = self.get('ItemGroup')
        refEl = etree.SubElement(itemg, self.namespace + 'Reference', {'Include': name})
        hintEl = etree.SubElement(refEl, self.namespace + 'HintPath')
        hintEl.text = path
        if SourcePath != None:
            sourceEl = etree.SubElement(refEl, self.namespace + 'SourcePath')
            sourceEl.text = SourcePath
    def add_reference_to_proj(self, path):
        targetproj = csproj(path)
        p = targetproj.get_props()

        path = self.get_canonical_path(path)
        
        itemg = self.get('ItemGroup')
        refEl = etree.SubElement(itemg, self.namespace + 'ProjectReference', {'Include': path})
        guidEl = etree.SubElement(refEl, self.namespace + 'Project')
        guidEl.text = p.guid
        nameEl = etree.SubElement(refEl, self.namespace + 'Name')
        nameEl.text = p.name
    def add_system_reference(self, name): # like System.Drawing or System.Windows.Forms
        itemg = self.get('ItemGroup')
        refEl = etree.SubElement(itemg, self.namespace + 'Reference', {'Include': name})

class csproj_props:
    def __init__(self, name, fver, type, guid):
        self.name = name
        self.fver = fver
        self.type = type
        self.guid = guid

class csproject_creator:
    def create(file, pr):
        text = csproject_creator.generate(pr)
        props.write_file(file, text)

    def generate(pr):
        re = csproject_creator.read_template()

        re = re.replace("#name#", pr.name)
        re = re.replace("#fver#", pr.fver)
        re = re.replace("#type#", pr.type)
        re = re.replace("#guid#", pr.guid)
        return re

    def read_template():
        return props.read_file(props.pjoin( props.script_dir, 'template.csproj' ))

    def get_guid():
        hex = string.digits + "ABCDEF"
        def rand_hex(len):
            lst = [random.choice(hex) for n in range(len)]
            return "".join(lst)
        return '{' + rand_hex(8) + '-' + rand_hex(4) + '-' + rand_hex(4) + '-' + rand_hex(4) + '-' + rand_hex(12) + '}'

