import os, string, re
import props
import slndata

class parse_methods:
    def get_preSolution(gl):
        start = 0
        while not gl[start].endswith('preSolution') and start < len(gl):
            start += 1

        end = start + 1
        while not gl[end].strip() == 'EndGlobalSection' and end >= 0:
            end += 1

        return gl[start:end + 1]
    def get_global(lines):
        for i in range(len(lines)):
            if(lines[i] == 'Global'):
                return lines[i+1:-1]

        raise("Wrong sln format")
    def get_projects_lines(lines):
        start = 0
        end = len(lines) - 1

        while not lines[start].startswith('Project') and start > len(lines):
            start += 1
        while not lines[end].startswith('EndProject') and end >= 0:
            end -= 1

        return lines[start:end + 1]
    
    guidre = re.compile(r"\{.{20,40}\}")
    namere = re.compile(r"[= ]\"[^,]+\"[, ]")
    def get_project_headers(lines):
        re = []
        for l in lines:
            if(l.strip() == 'EndProject'): continue
            guides = parse_methods.guidre.findall(l)
            names = parse_methods.namere.findall(l)
            re.append(slnProjInfo(names[0], names[1], guides[1], guides[0]))
            # print(re[-1])

        return re

    def get_pre_headers(pre):
        re = []
        for l in pre:
            p = l.strip('\t').split('=')
            if(p[0].startswith("GlobalSection") or p[0].startswith("EndGlobalSection")): continue
            p[0] = p[0].rstrip(' ')
            p[1] = p[1].lstrip(' ')
            re.append(p)
        return re

class slnProjInfo:
    def __init__(self, name, path, guid, typeguid):
        self.name = name.rstrip(', ').replace('\"', '').lstrip(' ')
        self.path = path.rstrip(', ').replace('\"', '').lstrip(' ')
        self.guid = guid
        self.typeguid = typeguid
    def __str__(self):
        return slndata.pheader.format(self.name, self.path, self.guid, self.typeguid)

class slnwriter:
    def __init__(self):
        self.txt = slndata.intro
        self.indent = 0

    def wl(self, line):
        self.txt += '\n' + ('\t' * self.indent)  + str(line)
    def weq(self, a, b):
        self.wl(a + ' = ' + b)
    def wpush(self, line):
        self.wl(line)
        self.push()
    def wpop(self, line):
        self.pop()
        self.wl(line)
    
    def push(self):
        self.indent += 1
    def pop(self):
        self.indent = max(0, self.indent - 1)

    def __str__(self): return self.txt

class slnobj:
    def __init__(self, file):
        if(file != None and os.path.isfile(file)):
            text = props.read_file(file)
            lines = text.split('\n')
            gl = parse_methods.get_global(lines)
            pr = parse_methods.get_projects_lines(lines)
            self.headers = parse_methods.get_project_headers(pr)

            pre = parse_methods.get_preSolution(gl)
            self.preh = parse_methods.get_pre_headers(pre)
        else:
            pre = slndata.default_headers
            self.preh = parse_methods.get_pre_headers(pre)
            self.headers = []
    
    def get_headers(): return self.headers
    def get_preh(): return self.preh

    def __str__(self):
        wr = slnwriter()

        for h in self.headers:
            wr.wl(h)

        wr.wpush("Global")
        wr.wpush("GlobalSection(SolutionConfigurationPlatforms) = preSolution")
        for h in self.preh:
            wr.weq(h[0], h[1])
        wr.wpop("EndGlobalSection")
        wr.wpush("GlobalSection(ProjectConfigurationPlatforms) = postSolution")

        for p in self.headers:
            for h2 in self.preh:
                for h in self.preh:
                    wr.weq(p.guid + '.' + h[0] + '.' + slndata.cfgs[0], h[1])
                    wr.weq(p.guid + '.' + h[0] + '.' + slndata.cfgs[1] + '.' + '0', h2[1])

        wr.wpop("EndGlobalSection")
        wr.wpop("EndGlobal")
        return str(wr)

class cssln(slnobj):
    def __init__(self, file):
        slnobj.__init__(self, file)

    def add_new_project(self, proj):
        self.headers.append(proj)