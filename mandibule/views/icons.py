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

from PySide import QtGui


class Icons(object):
    """Libraries of icons."""
    # NOTE: A class is used as a store here because the QApplication has to be
    # instanciated before QtGui.QIcon objects (causing a segmentation fault on
    # some systems like Ubuntu Lucid).
    def __init__(self, app):
        self.app = app
        self.icon_add = QtGui.QIcon.fromTheme('list-add')
        self.icon_edit = QtGui.QIcon.fromTheme('document-properties')
        self.icon_remove = QtGui.QIcon.fromTheme('list-remove')
        self.icon_exe = QtGui.QIcon.fromTheme('system-run')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
