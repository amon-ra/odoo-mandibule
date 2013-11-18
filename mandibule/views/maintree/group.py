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

from PySide import QtGui

from mandibule.utils.i18n import _
from mandibule.views.maintree.server import ServerItem


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
            self.add_server(sid, select=False)
        icon = QtGui.QIcon.fromTheme('folder')
        self.setIcon(0, icon)

    def update_group(self, id_):
        """Update the group identified by `ìd_`."""
        if self.id == id_:
            data = self.app.group_ctl.read(id_)
            self.setText(0, data['name'])

    def add_server(self, id_, select=True):
        """Add the server identified by `id_`."""
        data = self.app.server_ctl.read(id_)
        if self.id == data['group_id']:
            server = ServerItem(self.app, id_)
            self.addChild(server)
            server.setExpanded(True)
            if self.treeWidget() and select:
                self.treeWidget().setCurrentItem(server)

    def remove_server(self, id_):
        """Remove the server identified by `id_`."""
        for index in range(self.childCount()):
            server = self.child(index)
            if server.id == id_:
                server = self.takeChild(index)

    def get_menu(self):
        """Return a QMenu corresponding to the current GroupItem."""
        menu = QtGui.QMenu(self.treeWidget())
        # Add server
        icon_add = QtGui.QIcon.fromTheme('list-add')
        menu.addAction(
            icon_add,
            _("Add server"),
            self.app.server_ctl.display_form)
        # Remove current group
        icon_remove = QtGui.QIcon.fromTheme('list-remove')
        menu.addAction(
            icon_remove,
            _("Remove"),
            lambda: self.app.group_ctl.delete(self.id))
        # Properties
        menu.addSeparator()
        icon_properties = QtGui.QIcon.fromTheme('document-properties')
        menu.addAction(
            icon_properties,
            _("Properties"),
            lambda: self.app.group_ctl.display_form(self.id))
        return menu

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
