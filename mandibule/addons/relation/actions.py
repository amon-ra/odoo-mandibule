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
"""Add-on actions."""
from mandibule.reg import Action, Controller, UI
from mandibule.utils.i18n import _


class NewRelation(Action):
    """Action to add a new relation graph."""
    __metadata__ = {
        'name': 'new_relation',
        'icon': 'relation',
        'string': _(u"Add relational graph"),
        'shortcut': 'Ctrl+R',
        'server_menu': True,
    }

    def __connect__(self):
        UI['tree'].itemActivated.connect(self._update_state)

    def _update_state(self, item):
        if UI['tree'].current.get('server'):
            self.setDisabled(False)
        else:
            self.setDisabled(True)

    def run(self):
        """Display the form to add a relational graph."""
        if UI['tree'].current.get('server'):
            Controller['relation'].display_form()


class RemoveRelation(Action):
    """Action to remove a relation graph."""
    __metadata__ = {
        'name': 'remove_relation',
        'icon': 'remove',
        'string': _(u"Remove"),
    }

    def run(self):
        """Display the form to edit a relational graph."""
        id_ = UI['tree'].current.get('relation')
        if id_:
            Controller['relation'].delete_confirm(id_)


class EditRelation(Action):
    """Action to edit a relation graph."""
    __metadata__ = {
        'name': 'edit_relation',
        'icon': 'edit',
        'string': _(u"Modify"),
    }

    def run(self):
        """Display the form to edit a relational graph."""
        id_ = UI['tree'].current.get('relation')
        if id_:
            Controller['relation'].display_form(id_)


class ExecRelation(Action):
    """Action to execute a relation graph."""
    __metadata__ = {
        'name': 'exec_relation',
        'icon': 'exe',
        'string': _(u"Execute"),
    }

    def run(self):
        """Display the form to edit a relational graph."""
        id_ = UI['tree'].current.get('relation')
        if id_:
            Controller['relation'].display_form(id_)
            Controller['relation'].execute(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
