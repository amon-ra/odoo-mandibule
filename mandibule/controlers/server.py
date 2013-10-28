from PySide import QtGui, QtCore
from mandibule.controlers.funcmodule import FuncModule


class Server(object):
    def __init__(self, group, data):
        self.group = group
        self.name = data['name']
        self._funcs = {}
        self.item = QtGui.QTreeWidgetItem()
        self.item.setText(0, self.name)
        self.item.setData(0, QtCore.Qt.UserRole, self)
        for func, configs in getattr(self, 'funcs', {}).items():
            self.add_func_module(FuncModule(self.group, self, func, configs))


    def add_func_module(self, func_module):
        self.item.addChild(func_module.item)
        self._funcs[func_module.name] = func_module

    def remove_func_module(self, func_module):
        if not self._funcs[func_module.configs]:
            self.item.removeChild(func_module.item)
            del self._funcs[func_module.name]

    def update(self, data):
        self.name = data['name']
        self.item.setText(0, self.name)

    def serialize(self):
        out = {'name': self.name}
        funcs = getattr(self, 'funcs', False)
        if funcs:
            out['funcs'] = {}
            for func, configs in funcs:
                out['funcs'][func] = [conf.serialize() for conf in configs]
        return out

