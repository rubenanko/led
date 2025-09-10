from os.path import dirname, basename, isfile, join
import glob
import importlib
import sys

sys.path.append(dirname(__file__))
modules = glob.glob(join(dirname(__file__), "*.py"))
modules = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

def handle_modules(event : any)->bool:
    override = False
    for module in modules:
        if getattr(importlib.import_module(module),"entrypoint")(event): override = True
    
    return override
