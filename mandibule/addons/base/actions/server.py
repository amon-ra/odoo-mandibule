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
"""Server actions."""
from mandibule.reg import Action, Controller, UI
from mandibule.utils.i18n import _


class NewServer(Action):
    """Action to add a new server."""
    __metadata__ = {
        'name': 'new_server',
        'icon' : 'server',
        'string': _(u"New server"),
        'shortcut': 'Ctrl+H',
    }

    def run(self):
        """Display the form to add a new server."""
        Controller['server'].display_form()

    def __connect__(self):
        UI['tree'].currentItemChanged.connect(self._tree_item_changed)

    def _tree_item_changed(self, current, previous):
        """Enable/disable the action according to the current item selected
        in the main tree.
        """
        self.setDisabled(not current)


class RemoveServer(Action):
    """Action to remove a server."""
    __metadata__ = {
        'name': 'remove_server',
        'icon' : 'remove',
        'string': _(u"Remove"),
    }

    def run(self):
        """Remove the server."""
        id_ = UI['tree'].current.get('server')
        if id_:
            Controller['server'].delete_confirm(id_)


class EditServer(Action):
    """Action to edit a server."""
    __metadata__ = {
        'name': 'edit_server',
        'icon' : 'edit',
        'string': _(u"Modify"),
    }

    def run(self):
        """Display the form to edit a server."""
        id_ = UI['tree'].current.get('server')
        if id_:
            Controller['server'].display_form(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
