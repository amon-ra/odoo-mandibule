from PySide import QtGui, QtCore
from mandibule.serverlist.controlers.server import Server

class Group(object):
    def __init__(self, data):
        self.name = data['name']
        self._servers = []
        self.item = QtGui.QTreeWidgetItem()
        self.item.setText(0, self.name)
        self.item.setData(0, QtCore.Qt.UserRole, self)
        for elt in data.get('servers', []):
            self.add_server(Server(self, elt))

    def add_server(self, server):
        self.item.addChild(server.item)
        self._servers.append(server)

    def remove_server(self, server):
        self.item.removeChild(server.item)
        self._servers.remove(server)

    def update(self, data):
        self.name = data['name']
        self.item.setText(0, self.name)

    def serialize(self):
        out = {'name': self.name}
        if self._servers:
            out['servers'] = []
            for serv in self._servers:
                out['servers'].append(serv.serialize())
        return out
