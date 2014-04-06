# -*- coding: UTF-8 -*-
##############################################################################
#
#    Mandibule, an explorer for OpenERP servers
#    Copyright (C) 2013 Sébastien Alix
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
"""Defines standard actions."""
from PySide import QtGui

from mandibule.reg import Action
from mandibule.utils.i18n import _

from . import group
from . import server
from ..ui import about


class About(Action):
    """Action to display the 'about' dialog."""
    __metadata__ = {
        'name': 'about',
        'icon' : 'about',
        'string': _(u"About"),
    }

    def run(self):
        """Display the 'about' dialog."""
        about.display()


class Quit(Action):
    """Action to quit the application."""
    __metadata__ = {
        'name': 'quit',
        'icon' : 'quit',
        'string': _(u"Quit"),
        'shortcut': QtGui.QKeySequence.Quit,
    }

    def run(self):
        """Ask the user to confirm, and quit the application."""
        self.app.confirm_quit() and self.app.quit()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
