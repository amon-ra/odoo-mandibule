from mandibule.controlers.server import ServerControler
from mandibule.serverlistitem import ServerListItem


class GroupControler(object):
    """Controler for group items"""
    def __init__(self, serverlist, data):
        self.data = data
        self.serverlist_controler = serverlist
        self.servers = {}
        self.widget = ServerListItem(self, self.data['name'])
        for item in self.data.get('childs', []):
            self.add_server(item)

    def add_server(self, item):
        controler = ServerControler(self.serverlist_controler, self, item)
        self.widget.addChild(controler.widget)
        self.servers[item['name']] = controler

    def remove_server(self, server):
        self.widget.removeChild(server.widget)
        del self.servers[server.data['name']]

    def menu(self):
        return (
                ('New server', None),
                (None, None),
                ('Edit group', None),
                ('Remove group', None)
                )

