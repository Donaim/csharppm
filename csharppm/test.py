import os, props
import mxml
import pmanager as pm
from slnparser import slnobj
from slnmanager import slnmng
from lxml import etree # http://lxml.de/installation.html


def test_mxml():
    x = mxml.read_xml("tmp.csproj")
    props = x['Project']['PropertyGroup'][0]
    props['AssemblyName'] = 'LUL'
    # mxml.print_dict(props)

    mxml.write_xml('tmp.csproj', x)

def test_pmanager():
    p = pm.project('tmp.csproj')
    p.print('Project', 'PropertyGroup', 0)
    p.set('KEK1', 'Project', 'PropertyGroup', 0, 'AssemblyName')
    p.print('Project', 'PropertyGroup', 0)
    p.save()
def test_csproj():
    p = pm.csproj('tmp.csproj')
    p.add_reference('vutils/lul.dll')
    p.add_reference('hahaha/kek.dll')
    p.add_reference('ddd/aaaa/fuu.dll')
    p.save()
def test_sln():
    s = slnobj('tmp.sln')
    print(s)

def test_sln_manager():
    s = slnmng('DModuler.sln')
    s.create_project('lol/lol.csproj', 'COOLTYPE', 'VERSADD')
    s.create_reference('lol', '/home/d0naim/dev/vutils/vutils/bin/Release/vutils.dll')

def test_new_xml():
    root = etree.XML(props.read_file('tmp.csproj'))
    # print(root.tag)

    
    # ffff = mxml.find_tag('Optimize', root)
    ffff = mxml.find_all_tags('Optimize', root)
    print(ffff)

# make a copy
props.write_file('tmp.csproj', props.read_file(os.path.join(props.script_dir, 'template.csproj')))
props.write_file('tmp.sln', props.read_file(os.path.join(props.script_dir, 'template.sln')))

print("TESTING")
# test_mxml()
# test_pmanager()
# test_csproj()
# test_sln()
# test_sln_manager()
test_new_xml()
