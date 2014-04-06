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
"""Defines the main tree."""
from PySide import QtGui, QtCore

from mandibule.reg import Action, Controller, UI
from mandibule.addons.base.tree.group import GroupItem


class Tree(UI, QtGui.QTreeWidget):
    """Main tree to manage group, servers and functions."""
    __metadata__ = {
        'name': 'tree',
    }

    def __init__(self, app):
        UI.__init__(self, app)
        QtGui.QTreeWidget.__init__(self)
        self.setHeaderHidden(True)
        groups = Controller['group'].read_all()
        for id_ in sorted(groups, key=lambda gid: groups[gid]['name']):
            self._add_group('group', id_, select=False)
        self.setSortingEnabled(True)
        # Select the first group
        item = self.itemAt(0, 0)
        if item:
            self.setCurrentItem(item)

    def __connect__(self):
        Controller['group'].created.connect(
            lambda *args: self._add_group(*args))
        Controller['group'].deleted.connect(
            lambda *args: self._remove_group(*args))

    def _add_group(self, model, id_, select=True):
        """Add the group identified by `id_`."""
        group = GroupItem(self.app, id_, self)
        if select:
            self.setCurrentItem(group)

    def _remove_group(self, model, id_):
        """Remove the group identified by `id_`."""
        for index in range(self.topLevelItemCount()):
            group = self.topLevelItem(index)
            if group.id_ == id_:
                group = self.takeTopLevelItem(index)
                return

    @property
    def current(self):
        """Return a dictionary with active records of the tree following the
        current item selected::

            >>> UI['tree'].current
            {'group': '1385d48f5f5d4c29b9a2b9b83314b6f6',
             'server': '6ba3f7a9ef77442bbf318600b1e0fa6a',
             ...}
        """
        res = {}

        def process(item):
            item_id = item.__id__()
            if item_id:
                res.update([item_id])
            next_item = item.parent()
            if next_item:
                process(next_item)

        current = self.currentItem()
        if current:
            process(current)
        return res

    def contextMenuEvent(self, event):
        """Overridden to show a contextual menu according to the
        selected item.
        """
        if self.currentItem():
            menu = self.currentItem().__menu__()
            menu.popup(event.globalPos())
        else:
            menu = QtGui.QMenu(self)
            menu.addAction(Action['new_group'])
            menu.popup(event.globalPos())

    def mousePressEvent(self, event):
        """Overloaded to unset the current selection when clicking
        in the blanc area.
        """
        if self.itemAt(event.pos()) is None:
            self.setCurrentItem(None)
        QtGui.QTreeWidget.mousePressEvent(self, event)

    def keyPressEvent(self, event):
        """Overloaded to unset the current selection when pressing the
        Escape key.
        """
        if (event.key() == QtCore.Qt.Key_Escape and
            event.modifiers() == QtCore.Qt.NoModifier):
            self.setCurrentItem(None)
        else:
            QtGui.QTreeWidget.keyPressEvent(self, event)

    def rowsInserted(self, parent, start, end):
        """Overriden to automatically sort items when an item
        is added to the tree.
        """
        super(Tree, self).rowsInserted(parent, start, end)
        self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
