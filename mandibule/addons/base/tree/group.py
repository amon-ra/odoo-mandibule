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
"""Defines tree items for groups."""
from PySide import QtGui

from mandibule.reg import TreeItem, Controller, Icons, Action, UI


class GroupItem(TreeItem):
    """A group item inside the MainTree."""
    __metadata__ = {
        'name': 'group',
    }

    def __init__(self, app, id_, parent):
        TreeItem.__init__(self, app)
        parent.addTopLevelItem(self)
        self.id_ = id_
        data = Controller['group'].read(id_)
        self.setText(0, data['name'])
        servers = data.get('servers', {})
        for sid in sorted(servers, key=lambda sid: servers[sid]['name']):
            self._add_server('server', sid, select=False)
        self.setIcon(0, Icons['group'])
        # Set the visual state
        if self.childCount():
            self.setExpanded(True)

    def __id__(self):
        return ('group', self.id_)

    def __connect__(self):
        Controller['server'].created.connect(
            lambda *args: self._add_server(*args))
        Controller['server'].deleted.connect(
            lambda *args: self._remove_server(*args))
        Controller['server'].group_changed.connect(
            lambda *args: self._change_server_group(*args))
        Controller['group'].updated.connect(
            lambda *args: self._update(*args))
        UI['tree'].itemExpanded.connect(
            lambda *args: self._expand(*args))
        UI['tree'].itemCollapsed.connect(
            lambda *args: self._collapse(*args))

    def _expand(self, item):
        """Expand the menu item."""
        if self is item:
            self.set_icon_expanded(True)

    def _collapse(self, item):
        """Collapse the menu item."""
        if self is item:
            self.set_icon_expanded(False)

    def _update(self, model, id_):
        """Update the group identified by `ìd_`."""
        if self.id_ == id_:
            data = Controller['group'].read(id_)
            self.setText(0, data['name'])

    def _add_server(self, model, id_, select=True):
        """Add the server identified by `id_`."""
        data = Controller['server'].read(id_)
        if self.id_ == data['group_id']:
            server = TreeItem['server'](self.app, id_, self)
            if self.treeWidget() and select:
                self.treeWidget().setCurrentItem(server)

    def _remove_server(self, model, id_):
        """Remove the server identified by `id_`."""
        for index in range(self.childCount()):
            server = self.child(index)
            if server.id_ == id_:
                server = self.takeChild(index)
                self.set_icon_expanded()
                return

    def _change_server_group(self, model, id_, old_gid, new_gid):
        """Move the server in another group."""
        if self.id_ == old_gid:
            self.remove_server(id_)
        if self.id_ == new_gid:
            self._add_server(id_)

    def __menu__(self):
        """Return a QMenu corresponding to the current GroupItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(Action['new_server'])
        menu.addAction(Action['remove_group'])
        menu.addSeparator()
        menu.addAction(Action['edit_group'])
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        if expanded and self.childCount():
            self.setIcon(0, Icons['group_exp'])
        else:
            self.setIcon(0, Icons['group'])

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
