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

from PySide import QtCore, QtGui

from mandibule.utils.i18n import _
from mandibule.views.maintree import GroupItem, ServerItem, \
    RelationDrawer, DependencyDrawer, RelationItem, DependencyItem
from mandibule.views import about


class Actions(QtCore.QObject):
    """Libraries of actions."""
    def __init__(self, app):
        QtCore.QObject.__init__(self)
        self.app = app
        # Group
        self.action_new_group = QtGui.QAction(
            self.app.icons.icon_group_add, _("New group"), self.app)
        self.action_new_group.setShortcut('Ctrl+G')
        self.action_new_group.triggered.connect(self.new_group)
        self.action_remove_group = QtGui.QAction(
            self.app.icons.icon_remove, _("Remove"), self.app)
        self.action_remove_group.triggered.connect(self.remove_group)
        self.action_edit_group = QtGui.QAction(
            self.app.icons.icon_edit, _("Modify"), self.app)
        self.action_edit_group.triggered.connect(self.edit_group)
        # Server
        self.action_new_server = QtGui.QAction(
            self.app.icons.icon_server, _("New server"), self.app)
        self.action_new_server.setShortcut('Ctrl+H')
        self.action_new_server.triggered.connect(self.new_server)
        self.action_remove_server = QtGui.QAction(
            self.app.icons.icon_remove, _("Remove"), self.app)
        self.action_remove_server.triggered.connect(self.remove_server)
        self.action_edit_server = QtGui.QAction(
            self.app.icons.icon_edit, _("Modify"), self.app)
        self.action_edit_server.triggered.connect(self.edit_server)
        # Relation
        self.action_new_relation = QtGui.QAction(
            self.app.icons.icon_relation,
            _("Add relational graph"), self.app)
        self.action_new_relation.setShortcut('Ctrl+R')
        self.action_new_relation.triggered.connect(self.new_relation)
        self.action_remove_relation = QtGui.QAction(
            self.app.icons.icon_remove, _("Remove"), self.app)
        self.action_remove_relation.triggered.connect(self.remove_relation)
        self.action_edit_relation = QtGui.QAction(
            self.app.icons.icon_edit, _("Modify"), self.app)
        self.action_edit_relation.triggered.connect(self.edit_relation)
        self.action_exec_relation = QtGui.QAction(
            self.app.icons.icon_exe, _("Execute"), self.app)
        self.action_exec_relation.triggered.connect(self.exec_relation)
        # Dependency
        self.action_new_dependency = QtGui.QAction(
            self.app.icons.icon_dependencies,
            _("Add dependencies graph"), self.app)
        self.action_new_dependency.setShortcut('Ctrl+D')
        self.action_new_dependency.triggered.connect(self.new_dependency)
        self.action_remove_dependency = QtGui.QAction(
            self.app.icons.icon_remove, _("Remove"), self.app)
        self.action_remove_dependency.triggered.connect(self.remove_dependency)
        self.action_edit_dependency = QtGui.QAction(
            self.app.icons.icon_edit, _("Modify"), self.app)
        self.action_edit_dependency.triggered.connect(self.edit_dependency)
        self.action_exec_dependency = QtGui.QAction(
            self.app.icons.icon_exe, _("Execute"), self.app)
        self.action_exec_dependency.triggered.connect(self.exec_dependency)
        # About
        self.action_about = QtGui.QAction(
            self.app.icons.icon_about, _("About"), self.app)
        self.action_about.triggered.connect(lambda: about.display(self.app))
        # Quit
        self.action_quit = QtGui.QAction(
            self.app.icons.icon_quit, _("Quit"), self.app)
        self.action_quit.setShortcut('Ctrl+Q')
        self.action_quit.triggered.connect(self.app.quit)

    def update(self):
        """Enable/disable actions following the context."""
        if self.get_group_id():
            self.action_new_server.setDisabled(False)
        else:
            self.action_new_server.setDisabled(True)
        if self.get_server_id():
            self.action_new_relation.setDisabled(False)
            self.action_new_dependency.setDisabled(False)
        else:
            self.action_new_relation.setDisabled(True)
            self.action_new_dependency.setDisabled(True)

    def get_group_id(self):
        """Return the current group ID."""
        group_id = None
        current = self.app.main_tree.currentItem()
        if isinstance(current, GroupItem):
            group_id = current.id
        elif isinstance(current, ServerItem):
            group_id = current.parent().id
        elif isinstance(current, RelationDrawer) \
                or isinstance(current, DependencyDrawer):
            group_id = current.parent().parent().id
        elif isinstance(current, RelationItem) \
                or isinstance(current, DependencyItem):
            group_id = current.parent().parent().parent().id
        return group_id

    def get_server_id(self):
        """Return the current server ID."""
        server_id = None
        current = self.app.main_tree.currentItem()
        if isinstance(current, GroupItem):
            server_id = None
        elif isinstance(current, ServerItem):
            server_id = current.id
        elif isinstance(current, RelationDrawer) \
                or isinstance(current, DependencyDrawer):
            server_id = current.parent().id
        elif isinstance(current, RelationItem) \
                or isinstance(current, DependencyItem):
            server_id = current.parent().parent().id
        return server_id

    def get_relation_id(self):
        """Return the current relation graph ID."""
        current = self.app.main_tree.currentItem()
        if isinstance(current, RelationItem):
            return current.id

    def get_dependency_id(self):
        """Return the current dependencies graph ID."""
        current = self.app.main_tree.currentItem()
        if isinstance(current, DependencyItem):
            return current.id

    # -- Group --

    def new_group(self):
        """Display the form to add a group."""
        self.app.group_ctl.display_form()

    def remove_group(self):
        """Remove the current group."""
        id_ = self.get_group_id()
        self.app.group_ctl.delete(id_)

    def edit_group(self):
        """Display the form to edit a group."""
        id_ = self.get_group_id()
        self.app.group_ctl.display_form(id_)

    # -- Server --

    def new_server(self):
        """Display the form to add a server."""
        self.app.server_ctl.display_form()

    def remove_server(self):
        """Remove the current server."""
        id_ = self.get_server_id()
        self.app.server_ctl.delete_confirm(id_)

    def edit_server(self):
        """Display the form to edit a server."""
        id_ = self.get_server_id()
        self.app.server_ctl.display_form(id_)

    # -- Relation --

    def new_relation(self):
        """Display the form to add a relational graph."""
        self.app.relation_ctl.display_form()

    def remove_relation(self):
        """Remove the current relational graph."""
        id_ = self.get_relation_id()
        self.app.relation_ctl.delete_confirm(id_)

    def edit_relation(self):
        """Display the form to edit a relational graph."""
        id_ = self.get_relation_id()
        self.app.relation_ctl.display_form(id_)

    def exec_relation(self):
        """Generate the relational graph."""
        id_ = self.get_relation_id()
        self.app.relation_ctl.display_form(id_)
        self.app.relation_ctl.execute(id_)

    # -- Dependency --

    def new_dependency(self):
        """Display the form to add a dependencies graph."""
        self.app.dependency_ctl.display_form()

    def remove_dependency(self):
        """Remove the current relational graph."""
        id_ = self.get_dependency_id()
        self.app.dependency_ctl.delete_confirm(id_)

    def edit_dependency(self):
        """Display the form to edit a dependencies graph."""
        id_ = self.get_dependency_id()
        self.app.dependency_ctl.display_form(id_)

    def exec_dependency(self):
        """Generate the dependencies graph."""
        id_ = self.get_dependency_id()
        self.app.dependency_ctl.display_form(id_)
        self.app.dependency_ctl.execute(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
