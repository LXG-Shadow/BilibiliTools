from os.path import dirname, basename, isfile, join
from config import Config
import glob,importlib
modules = []

class BaseModule:
    def getMethod(self):
        return {}

    def getOptions(self):
        return {}

    def prepare(self):
        pass

    def process(self, args):
        pass

    def info(self,msg):
        print("BilibiliTools - %s > %s" %(self.__class__.__name__,msg))

for f in glob.glob(join(dirname(__file__), "*.py")):
    name = basename(f)[:-3:]
    if isfile(f) and not f.endswith('__init__.py') and name in Config.useModules:
        modules.append(importlib.import_module("."+name,"modules").module)
modules.sort(key=lambda m:Config.useModules.index(m.__name__))