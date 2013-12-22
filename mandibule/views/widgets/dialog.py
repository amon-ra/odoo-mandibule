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
"""Contains functions to pop-up useful dialogs to the user."""
from PySide import QtGui

from mandibule.utils.i18n import _


def confirm(parent, message, title=None):
    """Display a confirmation dialog (Yes/No response) and returns the
    boolean response.
    """
    if title is None:
        title = _(u"Confirmation")
    response = QtGui.QMessageBox.question(
        parent, title, message,
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    return response == QtGui.QMessageBox.Yes


def warning(parent, message, title=None):
    """Display a warning dialog."""
    if title is None:
        title = _(u"Warning")
    return QtGui.QMessageBox.warning(parent, title, message)


def error(parent, message, title=None):
    """Display an error dialog."""
    if title is None:
        title = _(u"Error")
    return QtGui.QMessageBox.critical(parent, title, message)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
