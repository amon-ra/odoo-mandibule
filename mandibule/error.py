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

import sys
import cStringIO, traceback

from PySide import QtGui


class ErrorHandler(QtGui.QMessageBox):
    """Handle error/exceptions raised by the application."""
    def __init__(self, app):
        QtGui.QMessageBox.__init__(self)
        self.app = app
        self.setIcon(QtGui.QMessageBox.Critical)
        sys.excepthook = self.excepthook

    def get_traceback_str(self, exc_traceback):
        """Return the string traceback extracted from `exc_traceback`."""
        traceback_str = cStringIO.StringIO()
        traceback.print_tb(exc_traceback, None, traceback_str)
        traceback_str.seek(0)
        return traceback_str.read()

    def excepthook(self, exc_type, exc_value, exc_traceback):
        """Exception hook bound to `sys.excepthook` which displayed a
        dialog to the user.
        """
        traceback_str = self.get_traceback_str(exc_traceback)
        self.setDetailedText(traceback_str)
        self.setText(unicode(exc_value))
        self.exec_()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
