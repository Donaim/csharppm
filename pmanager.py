import mxml
import json

class project:
    def __init__(self, file):
        self.file = file
        self.dict = mxml.read_xml(self.file)

    def save(self):
        mxml.write_xml(self.file, self.dict, pretty=True)
    def print(self):
        print(mxml.print_dict(self.dict))
    def print(self, *path):
        print(self.__getp(path))

    def __get(self, path):
        re = self.dict
        for i in path:
            re = re[i]
        return re
    def get(self, *path):
        return self.__get(path)
    def getp(self, *path):
        return self.__getp(path)
    def __getp(self, path):
        re = self.__get(path)
        return json.dumps(re, sort_keys=True, indent=4)
    
    def __set(self, val, path):
        re = self.dict
        for i in path[0:-1]:
            re = re[i]
        re[path[-1]] = val
    def set(self, val, *path):
        self.__set(val, path)