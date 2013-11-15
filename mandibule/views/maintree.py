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


class ServerItem(QtGui.QTreeWidgetItem):
    """A server item inside a GroupItem."""
    def __init__(self, app, id_):
        QtGui.QTreeWidgetItem.__init__(self)
        self.app = app
        self.app.server_ctl.updated.connect(self.update_server)
        self.id = id_
        data = self.app.server_ctl.read(id_)
        self.setText(0, data['name'])

    def update_server(self, id_):
        """Update the server identified by `ìd_`."""
        if self.id == id_:
            data = self.app.server_ctl.read(id_)
            self.setText(0, data['name'])


class GroupItem(QtGui.QTreeWidgetItem):
    """A group item inside the MainTree."""
    def __init__(self, app, id_):
        QtGui.QTreeWidgetItem.__init__(self)
        self.app = app
        self.app.server_ctl.created.connect(self.add_server)
        self.app.server_ctl.deleted.connect(self.remove_server)
        self.app.group_ctl.updated.connect(self.update_group)
        self.id = id_
        data = self.app.group_ctl.read(id_)
        self.setText(0, data['name'])
        for sid in data.get('servers', {}):
            self.add_server(sid)

    def update_group(self, id_):
        """Update the group identified by `ìd_`."""
        if self.id == id_:
            data = self.app.server_ctl.read(id_)
            self.setText(0, data['name'])

    def add_server(self, id_):
        """Add the server identified by `id_`."""
        data = self.app.server_ctl.read(id_)
        if self.id == data['group_id']:
            server = ServerItem(self.app, id_)
            self.addChild(server)
            server.setExpanded(True)

    def remove_server(self, id_):
        """Remove the server identified by `id_`."""
        for index in range(self.childCount()):
            server = self.child(index)
            if server.id == id_:
                server = self.takeChild(index)
                server.deleteLater()


class MainTree(QtGui.QTreeWidget):
    """Main tree to manage group, servers and functions."""
    def __init__(self, app):
        QtGui.QTreeWidget.__init__(self)
        self.app = app
        self.app.group_ctl.created.connect(self.add_group)
        self.app.group_ctl.deleted.connect(self.remove_group)
        # Header
        self.setHeaderLabel(_("OpenERP servers"))
        self.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter)
        for id_ in self.app.group_ctl.read_all():
            self.add_group(id_)

    def add_group(self, id_):
        """Add the group identified by `id_`."""
        group = GroupItem(self.app, id_)
        self.addTopLevelItem(group)
        group.setExpanded(True)

    def remove_group(self, id_):
        """Remove the group identified by `id_`."""
        for index in range(self.topLevelItemCount()):
            group = self.topLevelItem(index)
            if group.id == id_:
                group =self.takeTopLevelItem(index)
                group.deleteLater()

    #def contextMenuEvent(self, event):
    #    menu = QtGui.QMenu()
    #    menu.addAction(_("New group"), lambda x: x)
    #    menu.popup(event.globalPos())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
