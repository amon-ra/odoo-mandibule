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
"""Group actions."""
from mandibule.reg import Action, Controller, UI
from mandibule.utils.i18n import _


class NewGroup(Action):
    """Action to add a new group."""
    __metadata__ = {
        'name': 'new_group',
        'icon' : 'group',
        'string': _(u"New group"),
        'shortcut': 'Ctrl+G',
    }

    def run(self):
        """Display the form to add a new group."""
        Controller['group'].display_form()


class RemoveGroup(Action):
    """Action to remove a group."""
    __metadata__ = {
        'name': 'remove_group',
        'icon' : 'remove',
        'string': _(u"Remove"),
    }

    def run(self):
        """Remove the group."""
        id_ = UI['tree'].current.get('group')
        if id_:
            Controller['group'].delete_confirm(id_)


class EditGroup(Action):
    """Action to edit a group."""
    __metadata__ = {
        'name': 'edit_group',
        'icon' : 'edit',
        'string': _(u"Modify"),
    }

    def run(self):
        """Display the form to edit a group."""
        id_ = UI['tree'].current.get('group')
        if id_:
            Controller['group'].display_form(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
