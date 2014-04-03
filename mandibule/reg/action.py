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
"""Supply the `Action` base class and manage the registration of
actions with the `ActionRegister` class.
"""
from PySide import QtGui

from . import SingleRegister, Single
from .icon import Icons


class ActionRegister(SingleRegister):
    """Metaclass which register actions."""
    pass


class Action(Single, QtGui.QAction):
    """Base class to implement an action."""
    __metaclass__ = ActionRegister
    __metadata__ = {
        'name': None,
        'icon': None,
        'string': None,
        'shortcut': None,
        'shortcut_context': None,
        'server_menu': None,
    }

    def __init__(self, app):
        Single.__init__(self, app)
        if self.__metadata__.get('icon'):
            QtGui.QAction.__init__(
                self,
                Icons[self.__metadata__['icon']],
                self.__metadata__.get('string', u""),
                self.app)
        else:
            QtGui.QAction.__init__(
                self,
                self.__metadata__.get('string', u""),
                self.app)
        if self.__metadata__.get('shortcut'):
            self.setShortcut(self.__metadata__['shortcut'])
            if self.__metadata__.get('shortcut_context'):
                self.setShortcutContext(self.__metadata__['shortcut_context'])
        self.triggered.connect(lambda: self.run())

    def run(self):
        """Perform the action."""
        raise NotImplementedError

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
