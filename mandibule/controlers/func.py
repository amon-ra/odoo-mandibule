from mandibule.serverlistitem import ServerListItem



class FuncControler(object):
    """Controler for func items"""
    def __init__(self, serverlist, func_group, data):
        self.serverlist_controler = serverlist
        self.func_group = func_group
        self.data = data
        self.widget = ServerListItem(self, self.data['name'])

    def menu(self):
        return (
                ('Run...', None),
                (None, None),
                ('Edit functionality', None),
                ('Remove functionality', None)
                )
