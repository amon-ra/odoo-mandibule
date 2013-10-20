from mandibule import modules
from mandibule.controlers.funcgroup import FuncGroupControler
from mandibule.serverlistitem import ServerListItem



class ServerControler(object):
    """Controler for server items"""
    def __init__(self, serverlist, group, data):
        self.data = data
        self.group = group
        self.connected = False
        self.funcgroups = {}
        self.serverlist_controler = serverlist
        self.widget = ServerListItem(self, self.data['name'])
        for name, group in self.data.get('childs', {}).items():
            self.add_func_group(name, group)


    def add_func_group(self, name, item):
        controler = FuncGroupControler(self.serverlist_controler, self, name, item)
        self.widget.addChild(controler.widget)
        self.funcgroups[name] = controler

    def remove_func_group(self, func_group_controler):
        self.widget.removeChild(func_group_controler.widget)
        del self.funcgroups[func_group_controler.name]

    def menu(self):
        return (
                ('Connect' if not self.connected else 'Disconnect', None),
                ('New functionality', None),
                (None, None),
                ('Edit server', None),
                ('Remove server', None),
                )
