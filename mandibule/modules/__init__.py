from mandibule.modules import dependencies_graph, relations_graph

MODULES = (
        ('Dependencies', dependencies_graph),
        ('Relations', relations_graph),
        )

class ModuleNotFoundError(Exception):
    pass

def get_module(mod_name):
    for name, mod in MODULES:
        if name == mod_name:
            return mod
    raise ModuleNotFoundError(message=mod_name)
