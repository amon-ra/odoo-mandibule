# -*- coding: UTF-8 -*-
##############################################################################
#
#    Mandibule, an explorer for OpenERP servers
#    Copyright (C) 2014 Sébastien Alix
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
"""Defines the main window."""
from PySide import QtCore, QtGui

from mandibule.reg import UI

from . import tree
from . import workbook
from . import toolbar


class MainWindow(UI, QtGui.QMainWindow):
    """Main window."""
    __metadata__ = {
        'name': 'main_window',
    }

    def __init__(self, app):
        UI.__init__(self, app)
        QtGui.QMainWindow.__init__(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle('Mandibule!')
        self.setContentsMargins(0, 0, 0, 0)

        # Dockable main tree
        dock = QtGui.QDockWidget()
        dock.setMinimumSize(250, 250)
        dock.setWidget(tree.Tree(self.app))
        dock.setFeatures(dock.features() & ~dock.DockWidgetClosable)
        dock.setAllowedAreas(
            QtCore.Qt.RightDockWidgetArea|QtCore.Qt.LeftDockWidgetArea)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        self.setCentralWidget(workbook.WorkBook(self.app))
        self.addToolBar(toolbar.ToolBar(self.app))
        self.closeEvent = self._close_event
        self.aboutToQuit.connect(self._about_to_quit)
        self.show()

    def __connect__(self):
        self.aboutToQuit.connect(self._about_to_quit)

    def _close_event(self, event):
        """Override the 'QMainWindow.closeEvent()' method to check
        if the application can be closed.
        """
        if self.app.confirm_quit():
            event.accept()
        else:
            event.ignore()

    def _about_to_quit(self):
        """Method connected to the 'aboutToQuit' signal to wait for running
        threads before to quit.
        """
        self.hide()
        QtCore.QThreadPool.globalInstance().waitForDone()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
