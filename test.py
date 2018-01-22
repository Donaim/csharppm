import mxml
import pmanager as pm

def test_mxml():
    x = mxml.read_xml("tmp.csproj")
    props = x['Project']['PropertyGroup'][0]
    props['AssemblyName'] = 'LUL'
    # mxml.print_dict(props)

    mxml.write_xml('out.csproj', x)

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

# make a copy
mxml.write_file('tmp.csproj', mxml.read_file('shablon.csproj'))

# test_pmanager()
test_csproj()