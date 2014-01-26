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


class RelationItem(QtGui.QTreeWidgetItem):
    """A relational graph item inside a RelationDrawer."""
    def __init__(self, app, id_, parent):
        QtGui.QTreeWidgetItem.__init__(self)
        parent.addChild(self)
        self.app = app
        self.ctl = self.app.relation_ctl
        self.ctl.updated.connect(self.update_relation)
        self.id = id_
        data = self.ctl.read(id_)
        self.setText(0, data['name'])
        icon = QtGui.QIcon.fromTheme('system-run')
        self.setIcon(0, icon)

    def update_relation(self, id_):
        """Update the relational graph identified by `ìd_`."""
        if self.id == id_:
            data = self.ctl.read(id_)
            self.setText(0, data['name'])

    def get_menu(self):
        """Return a QMenu corresponding to the current RelationItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(self.app.actions.action_exec_relation)
        menu.addAction(self.app.actions.action_remove_relation)
        menu.addSeparator()
        menu.addAction(self.app.actions.action_edit_relation)
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        pass


class RelationDrawer(QtGui.QTreeWidgetItem):
    """A relational graph drawer item inside a ServerItem."""
    def __init__(self, app, server_id, parent):
        QtGui.QTreeWidgetItem.__init__(self)
        parent.addChild(self)
        self.app = app
        self.app.relation_ctl.created.connect(self.add_relation)
        self.app.relation_ctl.deleted.connect(self.remove_relation)
        self.server_id = server_id
        self.setText(0, _("Relations"))
        icon = QtGui.QIcon.fromTheme('folder')
        self.setIcon(0, icon)
        sdata = self.app.server_ctl.read(self.server_id)
        relations = sdata.get('relations', {})
        for rid in sorted(relations, key=lambda rid: relations[rid]['name']):
            self.add_relation(rid, select=False)
        if not self.childCount():
            self.setHidden(True)

    def add_relation(self, id_, select=True):
        """Add the relational graph identified by `id_`."""
        data = self.app.relation_ctl.read(id_)
        if self.server_id == data['server_id']:
            relation = RelationItem(self.app, id_, self)
            self.setHidden(False)
            self.setExpanded(True)
            if self.treeWidget() and select:
                self.treeWidget().setCurrentItem(relation)

    def remove_relation(self, id_):
        """Remove the relational graph identified by `id_`."""
        for index in range(self.childCount()):
            relation = self.child(index)
            if relation.id == id_:
                relation = self.takeChild(index)
                if not self.childCount():
                    self.setHidden(True)
                return

    def get_menu(self):
        """Return a QMenu corresponding to the current RelationItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(self.app.actions.action_new_relation)
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        if expanded and self.childCount():
            self.setIcon(0, self.app.icons.icon_group_exp)
        else:
            self.setIcon(0, self.app.icons.icon_group)

    def __lt__(self, other):
        """Avoid to sort drawers to keep the defined order."""
        return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
