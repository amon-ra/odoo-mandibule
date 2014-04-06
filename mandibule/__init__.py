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
__author__ = 'Sebastien Alix'
__email__ = 'seb@usr-src.org'
__licence__ = 'GPL v3'
__version__ = '0.2.0'

from PySide import QtGui, QtCore

from mandibule.reg import UI
from mandibule.utils.i18n import _
from mandibule import defaults
from mandibule.widgets import dialog
from mandibule.error import ErrorHandler
from mandibule import addons


class MainApp(QtGui.QApplication):
    """Main Qt application."""
    def __init__(self, argv):
        """ Initialize UI """
        super(MainApp, self).__init__(argv)
        self.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus, False)
        QtGui.QIcon.setThemeName('oxygen')
        # Application environment variables
        self.env = {}
        # Error handler
        self.error_handler = ErrorHandler(self)
        # Register addons
        addons.register(self)
        # Initialize the database and insert default values
        defaults.init(self)
        # Connect addons slots to signals
        addons.connect()
        self.aboutToQuit.connect(self._about_to_quit)

    def confirm_quit(self):
        """Return `True` if the application can be closed.
        If there is unsaved work, ask the user to confirm its action.
        """
        # Check unsaved work.
        confirm = True
        for content in UI['workbook'].tabs.itervalues():
            if content.unsaved:
                confirm = False
        for content in UI['workbook'].tabs_tmp.itervalues():
            if content.unsaved:
                confirm = False
        # Ask the user to confirm if unsaved work has been detected
        if not confirm:
            confirm = dialog.confirm(
                UI['main_window'],
                _(u"Unsaved work detected. Quit anyway?"),
                _(u"Unsaved work"))
        return confirm

    def _about_to_quit(self):
        """Method connected to the 'aboutToQuit' signal to wait for running
        threads before to quit.
        """
        UI['main_window'].hide()
        QtCore.QThreadPool.globalInstance().waitForDone()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
