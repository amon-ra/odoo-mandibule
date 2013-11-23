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


class DependencyItem(QtGui.QTreeWidgetItem):
    """A module dependencies graph item inside a DependencyDrawer."""
    def __init__(self, app, id_, parent):
        QtGui.QTreeWidgetItem.__init__(self)
        parent.addChild(self)
        self.app = app
        self.app.dependency_ctl.updated.connect(self.update_dependency)
        self.id = id_
        data = self.app.dependency_ctl.read(id_)
        self.setText(0, data['name'])
        icon = QtGui.QIcon.fromTheme('system-run')
        self.setIcon(0, icon)

    def update_dependency(self, id_):
        """Update the module dependencies graph identified by `ìd_`."""
        if self.id == id_:
            data = self.app.dependency_ctl.read(id_)
            self.setText(0, data['name'])

    def get_menu(self):
        """Return a QMenu corresponding to the current DependencyItem."""
        menu = QtGui.QMenu(self.treeWidget())
        # Execute the function
        icon_exe = QtGui.QIcon.fromTheme('system-run')
        menu.addAction(
            icon_exe,
            _("Execute"),
            lambda: self.app.dependency_ctl.execute(self.id))
        # Remove current module dependencies graph
        icon_remove = QtGui.QIcon.fromTheme('list-remove')
        menu.addAction(
            icon_remove,
            _("Remove"),
            lambda: self.app.dependency_ctl.delete(self.id))
        # Properties
        menu.addSeparator()
        icon_properties = QtGui.QIcon.fromTheme('document-properties')
        menu.addAction(
            icon_properties,
            _("Properties"),
            lambda: self.app.dependency_ctl.display_form(self.id))
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        pass


class DependencyDrawer(QtGui.QTreeWidgetItem):
    """A module dependencies graph drawer item inside a ServerItem."""
    def __init__(self, app, server_id, parent):
        QtGui.QTreeWidgetItem.__init__(self)
        parent.addChild(self)
        self.app = app
        self.app.dependency_ctl.created.connect(self.add_dependency)
        self.app.dependency_ctl.deleted.connect(self.remove_dependency)
        self.server_id = server_id
        self.setText(0, _("Module dependencies"))
        icon = QtGui.QIcon.fromTheme('folder')
        self.setIcon(0, icon)
        sdata = self.app.server_ctl.read(self.server_id)
        for rid in sdata.get('dependencies', {}):
            self.add_dependency(rid, select=False)
        if not self.childCount():
            self.setHidden(True)

    def add_dependency(self, id_, select=True):
        """Add the module dependencies graph identified by `id_`."""
        data = self.app.dependency_ctl.read(id_)
        if self.server_id == data['server_id']:
            dependency = DependencyItem(self.app, id_, self)
            self.setHidden(False)
            if self.treeWidget() and select:
                self.setExpanded(True)
                self.treeWidget().setCurrentItem(dependency)

    def remove_dependency(self, id_):
        """Remove the module dependencies graph identified by `id_`."""
        for index in range(self.childCount()):
            dependency = self.child(index)
            if dependency.id == id_:
                dependency = self.takeChild(index)
                if not self.childCount():
                    self.setHidden(True)
                return

    def get_menu(self):
        """Return a QMenu corresponding to the current DependencyItem."""
        menu = QtGui.QMenu(self.treeWidget())
        # Add module dependencies graph
        icon_add = QtGui.QIcon.fromTheme('list-add')
        menu.addAction(
            icon_add,
            _("Module dependencies graph"),
            lambda: self.app.dependency_ctl.display_form(None, self.server_id))
        return menu

    def set_icon_expanded(self, expanded=True):
        """Update the icon."""
        if expanded and self.childCount():
            self.setIcon(0, QtGui.QIcon.fromTheme('folder-open'))
        else:
            self.setIcon(0, QtGui.QIcon.fromTheme('folder'))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
