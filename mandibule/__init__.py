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

from mandibule.serverlist import ServerListControler
from mandibule.workarea import WorkAreaController
from mandibule import config
from mandibule.modules import MODULES


class MainApp(QtGui.QApplication):
    """Main Qt application."""
    def __init__(self, argv):
        """ Initialize UI """
        super(MainApp, self).__init__(argv)
        self.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus, False)

        # initialize widgets
        self.main_window = QtGui.QMainWindow()
        self.main_window.setWindowState(QtCore.Qt.WindowMaximized)
        self.serverlist = ServerListControler(self)
        self.workarea = WorkAreaController(self)

        # main window settings
        self.main_window.setWindowTitle('Mandibule !')
        self.main_window.setContentsMargins(0, 0, 0, 0)

        # splitter containing list of servers and working zone
        splitter = QtGui.QSplitter()
        splitter.addWidget(self.serverlist.widget)
        splitter.addWidget(self.workarea.widget)
        splitter.setSizes((100, 900))
        self.main_window.setCentralWidget(splitter)
        self.main_window.closeEvent = self._close
        self.main_window.show()

    @staticmethod
    def _close(event):
        """Called on main window closing."""
        print "DEBUG -> closing"
        event.accept()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
