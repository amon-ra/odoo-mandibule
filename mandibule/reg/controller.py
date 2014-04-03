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
"""Supply the `Controller` base class and manage the registration of
controllers with the `ControllerRegister` class.
"""
from PySide.QtCore import QObject

from . import SingleRegister, Single


class ControllerRegister(SingleRegister):
    """Metaclass which register all controllers of the application."""
    pass


class Controller(Single, QObject):
    """Base controller which defines common methods."""
    __metaclass__ = ControllerRegister
    __metadata__ = {
        'name': False,
        'function': False,
    }

    def __init__(self, app):
        Single.__init__(self, app)
        QObject.__init__(self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
