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
"""Add-on icons."""
from mandibule.reg import Icons

from PySide import QtGui


class BaseIcons(Icons):
    """Common icons."""
    __metadata__ = {
        'name': 'base',
    }

    def generate(self):
        return {
            'group_add': QtGui.QIcon.fromTheme('folder-new'),
            'group': QtGui.QIcon.fromTheme('folder'),
            'group_exp': QtGui.QIcon.fromTheme('folder-open'),
            'server': QtGui.QIcon.fromTheme('network-server'),
            'function': QtGui.QIcon.fromTheme('tab-new'),
            'add': QtGui.QIcon.fromTheme('list-add'),
            'export': QtGui.QIcon.fromTheme('document-export'),
            'save': QtGui.QIcon.fromTheme('document-save'),
            'undo': QtGui.QIcon.fromTheme('edit-undo'),
            'edit': QtGui.QIcon.fromTheme('document-properties'),
            'ok': QtGui.QIcon.fromTheme('dialog-ok'),
            'remove': QtGui.QIcon.fromTheme('list-remove'),
            'exe': QtGui.QIcon.fromTheme('system-run'),
            'wait': QtGui.QIcon.fromTheme('view-history'),
            'settings': QtGui.QIcon.fromTheme('preferences-other'),
            'about': QtGui.QIcon.fromTheme('help-about'),
            'quit': QtGui.QIcon.fromTheme('application-exit'),
            'zoom_in': QtGui.QIcon.fromTheme('zoom-in'),
            'zoom_out': QtGui.QIcon.fromTheme('zoom-out'),
            'zoom_orig': QtGui.QIcon.fromTheme('zoom-original'),
            'zoom_fit': QtGui.QIcon.fromTheme('zoom-fit-best'),
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
