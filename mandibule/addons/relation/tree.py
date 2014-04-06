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
"""Tree items."""
from PySide import QtGui

from mandibule.reg import TreeItem, Controller, Icons, Action, UI
from mandibule.utils.i18n import _


class RelationItem(TreeItem):
    """A relational graph item inside a RelationDrawer."""
    __metadata__ = {
        'name': 'relation',
    }

    def __init__(self, app, id_, parent):
        TreeItem.__init__(self, app)
        parent.addChild(self)
        self.id_ = id_
        data = Controller['relation'].read(id_)
        self.setText(0, data['name'])
        self.setIcon(0, Icons['exe'])

    def __id__(self):
        return ('relation', self.id_)

    def __connect__(self):
        Controller['relation'].updated.connect(
            lambda *args: self._update(*args))
        UI['tree'].itemDoubleClicked.connect(
            lambda *args: self._activated())
        UI['tree'].itemActivated.connect(
            lambda *args: self._activated())

    def _activated(self):
        """Open the workarea and execute the function."""
        if UI['tree'].current.get('relation') == self.id_:
            Controller['relation'].display_form(self.id_)
            Controller['relation'].execute(self.id_)

    def _update(self, model, id_, data):
        """Update the relational graph identified by `ìd_`."""
        if self.id_ == id_:
            self.setText(0, data['name'])

    def __menu__(self):
        """Return a QMenu corresponding to the current RelationItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(Action['exec_relation'])
        menu.addAction(Action['remove_relation'])
        menu.addSeparator()
        menu.addAction(Action['edit_relation'])
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        pass


class RelationDrawer(TreeItem):
    """A relational graph drawer item inside a ServerItem."""
    __metadata__ = {
        'name': 'relation_drawer',
        'append_to': 'server',
    }

    def __init__(self, app, server_id, parent):
        TreeItem.__init__(self, app)
        parent.addChild(self)
        self.server_id = server_id
        self.setText(0, _("Relations"))
        self.setIcon(0, Icons['group'])
        sdata = Controller['server'].read(self.server_id)
        relations = sdata.get('relations', {})
        for rid in sorted(relations, key=lambda rid: relations[rid]['name']):
            self._add('relation', rid, select=False)
        # Set the visual state
        if self.childCount():
            self.setExpanded(True)
            self.set_icon_expanded(True)
        else:
            self.setHidden(True)

    def __connect__(self):
        Controller['relation'].created.connect(
            lambda *args: self._add(*args))
        Controller['relation'].deleted.connect(
            lambda *args: self._remove(*args))
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

    def _add(self, model, id_, select=True):
        """Add the relational graph identified by `id_`."""
        data = Controller['relation'].read(id_)
        if self.server_id == data['server_id']:
            relation = RelationItem(self.app, id_, self)
            self.setHidden(False)
            self.setExpanded(True)
            if self.treeWidget() and select:
                self.treeWidget().setCurrentItem(relation)

    def _remove(self, model, id_):
        """Remove the relational graph identified by `id_`."""
        for index in range(self.childCount()):
            relation = self.child(index)
            if relation.id_ == id_:
                relation = self.takeChild(index)
                if not self.childCount():
                    self.setHidden(True)
                return

    def __menu__(self):
        """Return a QMenu corresponding to the current RelationItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(Action['new_relation'])
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        if expanded and self.childCount():
            self.setIcon(0, Icons['group_exp'])
        else:
            self.setIcon(0, Icons['group'])

    def __lt__(self, other):
        """Avoid to sort drawers to keep the defined order."""
        return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
