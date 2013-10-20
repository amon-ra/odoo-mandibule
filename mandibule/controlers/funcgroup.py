from mandibule.controlers.func import FuncControler
from mandibule.serverlistitem import ServerListItem



class FuncGroupControler(object):
    """Controler for funcs group items"""
    def __init__(self, serverlist, server, name, data):
        self.name = name
        self.data = data
        self.server = server
        self.serverlist_controler = serverlist
        self.funcs = {}
        self.widget = ServerListItem(self, self.name)
        for func in self.data:
            self.add_func(func)

    def add_func(self, func_data):
        controler = FuncControler(self.serverlist_controler, self, func_data)
        self.widget.addChild(controler.widget)
        self.funcs[controler.data['name']] = controler

    def remove_func(self, func_controler):
        self.widget.removeChild(func_controler.widget)
        del self.funcs[func_controler.data['name']]

    def menu(self):
        return None

