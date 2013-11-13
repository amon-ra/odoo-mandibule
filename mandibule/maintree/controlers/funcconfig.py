# -*- coding: UTF-8 -*-
##############################################################################
#
#    Mandibule, an explorer for OpenERP servers
#    Copyright (C) 2013 Sébastien Alix
#                       Frédéric Fidon
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
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
        # Execute
        icon_run = QtGui.QIcon.fromTheme('system-run')
        menu.addAction(icon_run, _("Execute"), ref._exec_func)
        # Remove
        icon_remove = QtGui.QIcon.fromTheme('list-remove')
        menu.addAction(icon_remove, _("Remove"), ref._remove_func)
        # Properties
        menu.addSeparator()
        icon_properties = QtGui.QIcon.fromTheme('document-properties')
        menu.addAction(icon_properties, _("Properties"), ref._edit_func)
        return menu

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
