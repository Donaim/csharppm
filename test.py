import mxml
import pmanager

x = mxml.read_xml("shablon.csproj")
props = x['Project']['PropertyGroup'][0]
props['AssemblyName'] = 'LUL'
# mxml.print_dict(props)

mxml.write_xml('out.csproj', x)