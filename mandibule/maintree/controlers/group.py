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

from mandibule.maintree.controlers.server import Server
from mandibule.utils.i18n import _


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

    def get_menu(self, ref):
        menu = QtGui.QMenu(ref.widget)
        # Add group
        icon_add = QtGui.QIcon.fromTheme('list-add')
        menu.addAction(icon_add, _("Add group"), ref._new_group)
        # Add server
        menu.addAction(icon_add, _("Add server"), ref._new_server)
        # Remove current group
        icon_remove = QtGui.QIcon.fromTheme('list-remove')
        menu.addAction(icon_remove, _("Remove"), ref._remove_group)
        # Properties
        menu.addSeparator()
        icon_properties = QtGui.QIcon.fromTheme('document-properties')
        menu.addAction(icon_properties, _("Properties"), ref._edit_group)
        return menu

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
