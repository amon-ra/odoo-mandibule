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


class ToolBar(QtGui.QToolBar):
    """Main toolbar."""
    def __init__(self, app):
        QtGui.QToolBar.__init__(self)
        self.app = app
        self.app.main_tree.currentItemChanged.connect(self._tree_item_changed)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.action_functions = QtGui.QAction(
            self.app.icons.icon_function, _("Functions"), self)
        # Add actions to the toolbar
        self.addAction(self.app.actions.action_new_group)
        self.addAction(self.app.actions.action_new_server)
        self.addAction(self.action_functions)
        separator = QtGui.QWidget()
        separator.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.addWidget(separator)
        #self.addAction(self._actions['settings'])
        self.addAction(self.app.actions.action_about)
        self.addAction(self.app.actions.action_quit)
        # Add a submenu on the 'functions' tool button
        fmenu = QtGui.QMenu()
        fmenu.addAction(self.app.actions.action_new_relation)
        fmenu.addAction(self.app.actions.action_new_dependency)
        self.action_functions.setMenu(fmenu)
        for widget in self.action_functions.associatedWidgets():
            if isinstance(widget, QtGui.QToolButton):
                widget.setPopupMode(QtGui.QToolButton.InstantPopup)

    def _tree_item_changed(self, current, previous):
        """Enable/disable actions of the toolbar according to the current
        item selected in the main tree.
        """
        if self.app.actions.get_server_id():
            self.action_functions.setDisabled(False)
        else:
            self.action_functions.setDisabled(True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
