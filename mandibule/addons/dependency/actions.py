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


class NewDependency(Action):
    """Action to add a new dependencies graph."""
    __metadata__ = {
        'name': 'new_dependency',
        'icon': 'dependency',
        'string': _(u"Add dependencies graph"),
        'shortcut': 'Ctrl+D',
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
        """Display the form to add a dependencies graph."""
        if UI['tree'].current.get('server'):
            Controller['dependency'].display_form()


class RemoveDependency(Action):
    """Action to remove a dependencies graph."""
    __metadata__ = {
        'name': 'remove_dependency',
        'icon': 'remove',
        'string': _(u"Remove"),
    }

    def run(self):
        """Display the form to edit a dependencies graph."""
        id_ = UI['tree'].current.get('dependency')
        if id_:
            Controller['dependency'].delete_confirm(id_)


class EditDependency(Action):
    """Action to edit a dependencies graph."""
    __metadata__ = {
        'name': 'edit_dependency',
        'icon': 'edit',
        'string': _(u"Modify"),
    }

    def run(self):
        """Display the form to edit a dependencies graph."""
        id_ = UI['tree'].current.get('dependency')
        if id_:
            Controller['dependency'].display_form(id_)


class ExecDependency(Action):
    """Action to execute a dependencies graph."""
    __metadata__ = {
        'name': 'exec_dependency',
        'icon': 'exe',
        'string': _(u"Execute"),
    }

    def run(self):
        """Display the form to edit a dependencies graph."""
        id_ = UI['tree'].current.get('dependency')
        if id_:
            Controller['dependency'].display_form(id_)
            Controller['dependency'].execute(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
