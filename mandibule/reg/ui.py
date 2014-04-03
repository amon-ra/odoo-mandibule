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
"""Supply the `UI` base class and manage the registration of the
main user interface widgets with the `UIRegister` class.
"""
from . import SingleRegister, Single


class UIRegister(SingleRegister):
    """Metaclass which register UI widgets."""
    pass


class UI(Single):
    """Base class to implement a UI widget."""
    __metaclass__ = UIRegister
    __metadata__ = {
        'name': False,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
