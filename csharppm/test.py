import os, props
import mxml
import pmanager as pm
from slnparser import slnobj


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


# make a copy
props.write_file('tmp.csproj', props.read_file(os.path.join(props.script_dir, 'template.csproj')))
props.write_file('tmp.sln', props.read_file(os.path.join(props.script_dir, 'template.sln')))

print("TESTING")
# test_pmanager()
# test_csproj()
test_sln()
