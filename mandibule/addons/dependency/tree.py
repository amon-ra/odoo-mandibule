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


class DependencyItem(TreeItem):
    """A module dependencies graph item inside a DependencyDrawer."""
    __metadata__ = {
        'name': 'dependency',
    }

    def __init__(self, app, id_, parent):
        TreeItem.__init__(self, app)
        parent.addChild(self)
        self.id_ = id_
        data = Controller['dependency'].read(id_)
        self.setText(0, data['name'])
        self.setIcon(0, Icons['exe'])

    def __id__(self):
        return ('dependency', self.id_)

    def __connect__(self):
        Controller['dependency'].updated.connect(
            lambda *args: self._update(*args))
        UI['tree'].itemDoubleClicked.connect(
            lambda *args: self._activated())
        UI['tree'].itemActivated.connect(
            lambda *args: self._activated())

    def _activated(self):
        """Open the workarea and execute the function."""
        if UI['tree'].current.get('dependency') == self.id_:
            Controller['dependency'].display_form(self.id_)
            Controller['dependency'].execute(self.id_)

    def _update(self, model, id_, data):
        """Update the module dependencies graph identified by `ìd_`."""
        if self.id_ == id_:
            self.setText(0, data['name'])

    def __menu__(self):
        """Return a QMenu corresponding to the current DependencyItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(Action['exec_dependency'])
        menu.addAction(Action['remove_dependency'])
        menu.addSeparator()
        menu.addAction(Action['edit_dependency'])
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        pass


class DependencyDrawer(TreeItem):
    """A module dependencies graph drawer item inside a ServerItem."""
    __metadata__ = {
        'name': 'dependency_drawer',
        'append_to': 'server',
    }

    def __init__(self, app, server_id, parent):
        TreeItem.__init__(self, app)
        parent.addChild(self)
        self.server_id = server_id
        self.setText(0, _("Dependencies"))
        self.setIcon(0, Icons['group'])
        sdata = Controller['server'].read(self.server_id)
        dependencies = sdata.get('dependencies', {})
        for did in sorted(
                dependencies, key=lambda did: dependencies[did]['name']):
            self._add('dependency', did, select=False)
        # Set the visual state
        if self.childCount():
            self.setExpanded(True)
            self.set_icon_expanded(True)
        else:
            self.setHidden(True)

    def __connect__(self):
        Controller['dependency'].created.connect(
            lambda *args: self._add(*args))
        Controller['dependency'].deleted.connect(
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
        """Add the module dependencies graph identified by `id_`."""
        data = Controller['dependency'].read(id_)
        if self.server_id == data['server_id']:
            dependency = DependencyItem(self.app, id_, self)
            self.setHidden(False)
            self.setExpanded(True)
            if self.treeWidget() and select:
                self.treeWidget().setCurrentItem(dependency)

    def _remove(self, model, id_):
        """Remove the module dependencies graph identified by `id_`."""
        for index in range(self.childCount()):
            dependency = self.child(index)
            if dependency.id_ == id_:
                dependency = self.takeChild(index)
                if not self.childCount():
                    self.setHidden(True)
                return

    def __menu__(self):
        """Return a QMenu corresponding to the current DependencyItem."""
        menu = QtGui.QMenu(self.treeWidget())
        menu.addAction(Action['new_dependency'])
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
