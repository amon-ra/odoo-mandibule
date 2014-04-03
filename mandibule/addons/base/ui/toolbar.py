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
"""Defines the toolbar of the main window."""
from PySide import QtGui, QtCore

from mandibule.reg import Action, Icons, UI
from mandibule.utils.i18n import _


class ToolBar(UI, QtGui.QToolBar):
    """Main toolbar."""
    __metadata__ = {
        'name': 'toolbar',
    }

    def __init__(self, app):
        UI.__init__(self, app)
        QtGui.QToolBar.__init__(self)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.action_functions = QtGui.QAction(
            Icons['function'], _("Functions"), self)
        self.action_functions.setDisabled(True)
        # Add actions to the toolbar
        self.addAction(Action['new_group'])
        self.addAction(Action['new_server'])
        self.addAction(self.action_functions)
        separator = QtGui.QWidget()
        separator.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.addWidget(separator)
        #self.addAction(self._actions['settings'])
        self.addAction(Action['about'])
        self.addAction(Action['quit'])
        # Add a submenu on the 'functions' tool button
        fmenu = QtGui.QMenu()
        fmenu.addAction(Action['new_relation'])
        fmenu.addAction(Action['new_dependency'])
        self.action_functions.setMenu(fmenu)
        for widget in self.action_functions.associatedWidgets():
            if isinstance(widget, QtGui.QToolButton):
                widget.setPopupMode(QtGui.QToolButton.InstantPopup)

    def __connect__(self):
        UI['tree'].currentItemChanged.connect(self._tree_item_changed)

    def _tree_item_changed(self, current, previous):
        """Enable/disable actions of the toolbar according to the current
        item selected in the main tree.
        """
        if (not current) or \
                (current and current.__metadata__['name'] == 'group'):
            self.action_functions.setDisabled(True)
        else:
            self.action_functions.setDisabled(False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
