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
"""Supply the `WorkArea` base class and manage the registration of
work areas with the `WorkAreaRegister` class.
"""
from PySide import QtGui

from . import MultiRegister, Multi


class WorkAreaRegister(MultiRegister):
    """Metaclass which register work areas."""
    pass


class WorkArea(Multi, QtGui.QWidget):
    """Base class to implement a workarea."""
    __metaclass__ = WorkAreaRegister
    __metadata__ = {
        'name': False,
    }

    def __init__(self, app):
        Multi.__init__(self, app)
        QtGui.QWidget.__init__(self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
