

intro = \
"""﻿
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio 15
VisualStudioVersion = 15.0.26228.9
MinimumVisualStudioVersion = 10.0.40219.1"""

pheader = \
"""Project("{}") = "{}", "{}", "{}"
EndProject"""


cfgs = ("ActiveCfg", "Build")

default_headers = [
"Release|Any CPU = Release|Any CPU",
"Release|x64 = Release|x64",
"Release|x86 = Release|x86",
"Debug|Any CPU = Debug|Any CPU",
"Debug|x64 = Debug|x64",
"Debug|x86 = Debug|x86",
]

