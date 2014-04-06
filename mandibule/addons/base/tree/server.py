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
"""Defines tree items for servers."""
from PySide import QtGui

from mandibule.reg import TreeItem, Controller, Icons, Action


class ServerItem(TreeItem):
    """A server item inside a GroupItem."""
    __metadata__ = {
        'name': 'server',
    }

    def __init__(self, app, id_, parent):
        TreeItem.__init__(self, app)
        parent.addChild(self)
        self.id_ = id_
        data = Controller['server'].read(id_)
        self.setText(0, data['name'])
        self.setIcon(0, Icons['server'])
        # Add the drawers
        for name in TreeItem:
            Item = TreeItem[name]
            if Item.__metadata__.get('append_to') is 'server':
                self.addChild(Item(self.app, self.id_, self))

    def __id__(self):
        return ('server', self.id_)

    def __connect__(self):
        Controller['server'].updated.connect(
            lambda *args: self._update(*args))

    def _update(self, model, id_):
        """Update the server identified by `ìd_`."""
        if self.id_ == id_:
            data = Controller['server'].read(self.id_)
            self.setText(0, data['name'])

    def __menu__(self):
        """Return a QMenu corresponding to the current ServerItem."""
        menu = QtGui.QMenu(self.treeWidget())
        for name in Action:
            action = Action[name]
            if action.__metadata__.get('server_menu'):
                menu.addAction(action)
        menu.addSeparator()
        menu.addAction(Action['remove_server'])
        menu.addAction(Action['edit_server'])
        return menu

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
