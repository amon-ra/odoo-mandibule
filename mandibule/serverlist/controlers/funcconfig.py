from PySide import QtGui, QtCore
from mandibule.utils.i18n import _


class FuncConfig(object):
    def __init__(self, group, server, func_module, data):
        self.group = group
        self.server = server
        self.func_module = func_module
        self.name = data['name']
        self.data = data
        self.item = QtGui.QTreeWidgetItem()
        self.item.setText(0, self.name)
        self.item.setData(0, QtCore.Qt.UserRole, self)


    def update(self, data):
        self.data = data
        self.name = data['name']
        self.item.setText(0, self.name)

    def serialize(self):
        return self.data

    def get_menu(self, ref):
        menu = QtGui.QMenu(ref.widget)
        menu.addAction(_("Edit function"), ref._edit_func)
        menu.addAction(_("Remove function"), ref._remove_func)
        menu.addSeparator()
        menu.addAction(_("Execute function"), ref._exec_func)
        return menu
