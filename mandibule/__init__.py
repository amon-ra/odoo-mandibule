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

from mandibule.controllers import GroupController, ServerController
from mandibule.views import MainTree
from mandibule.maintree import MainTree as MainTree2  # FIXME temporary renamed
from mandibule.workarea import WorkAreaController
from mandibule import config


class MainApp(QtGui.QApplication):
    """Main Qt application."""
    def __init__(self, argv):
        """ Initialize UI """
        super(MainApp, self).__init__(argv)
        self.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus, False)
        QtGui.QIcon.setThemeName('oxygen')
        # Controllers
        self.group_ctl = GroupController(self)
        self.server_ctl = ServerController(self)
        # Views
        self.main_window = QtGui.QMainWindow()
        self.main_window.setWindowState(QtCore.Qt.WindowMaximized)
        self.main_window.setWindowTitle('Mandibule !')
        self.main_window.setContentsMargins(0, 0, 0, 0)
        self.main_tree = MainTree(self)

        # == TODO code below need review ==

        # initialize widgets
        self.main_tree_old = MainTree2(self)
        self.workarea = WorkAreaController(self)

        # Dockable maintree
        dock = QtGui.QDockWidget('OpenERP servers')
        dock.setMinimumSize(250, 250)
        dock.setWidget(self.main_tree)
        dock.setFeatures(dock.features() & ~dock.DockWidgetClosable)
        dock.setAllowedAreas(
            QtCore.Qt.RightDockWidgetArea|QtCore.Qt.LeftDockWidgetArea)
        self.main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        # FIXME Legacy dockable maintree (remove later)
        dock_old = QtGui.QDockWidget('OpenERP servers')
        dock_old.setMinimumSize(250, 250)
        dock_old.setWidget(self.main_tree_old.widget)
        dock_old.setFeatures(dock_old.features() & ~dock_old.DockWidgetClosable)
        dock_old.setAllowedAreas(
            QtCore.Qt.RightDockWidgetArea|QtCore.Qt.LeftDockWidgetArea)
        self.main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_old)

        self.main_window.setCentralWidget(self.workarea.widget)
        self.main_window.closeEvent = self._close
        self.main_window.show()

    @staticmethod
    def _close(event):
        """Called on main window closing."""
        print "DEBUG -> closing"
        event.accept()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
