from PySide import QtGui, QtCore
from mandibule.controlers.funcconfig import FuncConfig

class FuncModule(object):
    def __init__(self, group, server, name, configs):
        self.group = group
        self.server = server
        self.name = name
        self.configs = configs
        self.item = QtGui.QTreeWidgetItem()
        self.item.setText(0, self.name)
        self.item.setData(0, QtCore.Qt.UserRole, self)
        for config in self.configs:
            self.add_config(FuncConfig(self.group, self.server, self, config))


    def add_config(self, config):
        self.item.addChild(config.item)

    def remove_config(self, config):
        self.item.removeChild(config.item)
