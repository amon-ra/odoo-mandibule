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
"""Supply the `TreeItem` base class and manage the registration of tree items
with the `TreeItemRegister` class.
"""
from PySide import QtGui

from . import MultiRegister, Multi


class TreeItemRegister(MultiRegister):
    """Metaclass which register tree items."""
    pass


class TreeItem(Multi, QtGui.QTreeWidgetItem):
    """Base class to implement a menu item."""
    __metaclass__ = TreeItemRegister
    __metadata__ = {
        'name': None,
        'append_to': False,
    }

    def __init__(self, app):
        Multi.__init__(self, app)
        QtGui.QTreeWidgetItem.__init__(self)

    def __id__(self):
        """Return a tuple `(model, ID)` which identify the record used by the
        tree item. If the tree item is not based on a specific record, returns
        `None`.
        """
        pass

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
