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
from mandibule.views.maintree import GroupItem, ServerItem, \
    RelationDrawer, DependencyDrawer, RelationItem, DependencyItem


class ToolBar(QtGui.QToolBar):
    """Main toolbar."""
    def __init__(self, app):
        QtGui.QToolBar.__init__(self)
        self.app = app
        self.app.main_tree.currentItemChanged.connect(self.tree_item_changed)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    def tree_item_changed(self, current, previous):
        self.clear()
        if current is None:
            # New group
            self.addAction(
                self.app.icons.icon_add,
                _("New group"),
                self.app.group_ctl.display_form)
        elif isinstance(current, GroupItem):
            # New group
            self.addAction(
                self.app.icons.icon_add,
                _("New group"),
                self.app.group_ctl.display_form)
            self.addSeparator()
            # Edit group
            self.addAction(
                self.app.icons.icon_edit,
                _("Properties"),
                lambda: self.app.group_ctl.display_form(current.id))
            # Remove group
            self.addAction(
                self.app.icons.icon_remove,
                _("Remove"),
                lambda: self.app.group_ctl.delete(current.id))
            self.addSeparator()
            # New server
            self.addAction(
                self.app.icons.icon_add,
                _("New server"),
                lambda: self.app.server_ctl.display_form(None, current.id))
        elif isinstance(current, ServerItem):
            # New server
            self.addAction(
                self.app.icons.icon_add,
                _("New server"),
                lambda: self.app.server_ctl.display_form(
                    None, current.parent().id))
            self.addSeparator()
            # Edit server
            self.addAction(
                self.app.icons.icon_edit,
                _("Properties"),
                lambda: self.app.server_ctl.display_form(current.id))
            # Remove server
            self.addAction(
                self.app.icons.icon_remove,
                _("Remove"),
                lambda: self.app.server_ctl.delete(current.id))
            self.addSeparator()
            # Add relational graph
            self.addAction(
                QtGui.QIcon.fromTheme('view-time-schedule'),
                _("Add relational graph"),
                lambda: self.app.relation_ctl.display_form(None, current.id))
            # Add module dependencies graph
            self.addAction(
                QtGui.QIcon.fromTheme('view-list-tree'),
                _("Add dependencies graph"),
                lambda: self.app.dependency_ctl.display_form(None, current.id))
        elif isinstance(current, RelationDrawer) \
                or isinstance(current, DependencyDrawer):
            # New server
            self.addAction(
                self.app.icons.icon_add,
                _("New server"),
                lambda: self.app.server_ctl.display_form(
                    None, current.parent().parent().id))
            self.addSeparator()
            # Edit server
            self.addAction(
                self.app.icons.icon_edit,
                _("Properties"),
                lambda: self.app.server_ctl.display_form(current.parent().id))
            # Remove server
            self.addAction(
                self.app.icons.icon_remove,
                _("Remove"),
                lambda: self.app.server_ctl.delete(current.parent().id))
            self.addSeparator()
            # Add relational graph
            self.addAction(
                QtGui.QIcon.fromTheme('view-time-schedule'),
                _("Add relational graph"),
                lambda: self.app.relation_ctl.display_form(
                    None, current.parent().id))
            # Add module dependencies graph
            self.addAction(
                QtGui.QIcon.fromTheme('view-list-tree'),
                _("Add dependencies graph"),
                lambda: self.app.dependency_ctl.display_form(
                    None, current.parent().id))
        elif isinstance(current, RelationItem):
            # New server
            self.addAction(
                self.app.icons.icon_add,
                _("New server"),
                lambda: self.app.server_ctl.display_form(
                    None, current.parent().parent().parent().id))
            self.addSeparator()
            # Edit function
            self.addAction(
                self.app.icons.icon_edit,
                _("Properties"),
                lambda: self.app.relation_ctl.display_form(current.id))
            # Remove function
            self.addAction(
                self.app.icons.icon_remove,
                _("Remove"),
                lambda: self.app.relation_ctl.delete(current.id))
            self.addSeparator()
            # Execute the function
            self.addAction(
                self.app.icons.icon_exe,
                _("Execute"),
                lambda: self.app.relation_ctl.execute(current.id))
        elif isinstance(current, DependencyItem):
            # New server
            self.addAction(
                self.app.icons.icon_add,
                _("New server"),
                lambda: self.app.server_ctl.display_form(
                    None, current.parent().parent().parent().id))
            self.addSeparator()
            # Edit function
            self.addAction(
                self.app.icons.icon_edit,
                _("Properties"),
                lambda: self.app.dependency_ctl.display_form(current.id))
            # Remove function
            self.addAction(
                self.app.icons.icon_remove,
                _("Remove"),
                lambda: self.app.dependency_ctl.delete(current.id))
            self.addSeparator()
            # Execute the function
            self.addAction(
                self.app.icons.icon_exe,
                _("Execute"),
                lambda: self.app.dependency_ctl.execute(current.id))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
