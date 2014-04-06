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
"""Defines the group form."""
from PySide import QtGui

from mandibule.reg import Controller, UI
from mandibule.utils.i18n import _
from mandibule.widgets.fields import \
    TextField, SelectField, IntField, PasswordField


class ServerForm(QtGui.QDialog):
    """Server form."""
    def __init__(self, app, id_=None, data=None):
        QtGui.QDialog.__init__(self)
        self.app = app
        self.id_ = id_
        self.data = data
        self.fields = {}
        self.setLayout(QtGui.QFormLayout())
        groups = Controller['group'].read_all()
        group_id = data and data.get('group_id') \
            or UI['tree'].current.get('group')
        # Fields
        self.fields['name'] = TextField(_("Name"), data.get('name', ''))
        self.layout().addRow(
            self.fields['name'].label, self.fields['name'].widget)
        self.fields['group'] = SelectField(
            _("Group"),
            [(group['name'], gid) for gid, group in groups.iteritems()],
            group_id)
        self.layout().addRow(
            self.fields['group'].label, self.fields['group'].widget)
        self.fields['server'] = TextField(
            _("Host"), data.get('oerplib', {}).get('server', ''))
        self.layout().addRow(
            self.fields['server'].label, self.fields['server'].widget)
        self.fields['protocol'] = SelectField(
            _("Protocol"),
            [("XML-RPC", 'xmlrpc'),
             ("XML-RPC + SSL", 'xmlrpc+ssl'),
             ("Net-RPC", 'netrpc')],
            data.get('oerplib', {}).get('protocol', 'xmlrpc'))
        self.layout().addRow(
            self.fields['protocol'].label, self.fields['protocol'].widget)
        self.fields['port'] = IntField(
            _("Port"),
            data.get('oerplib', {}).get('port', 8069),
            range_=(1, 65535))
        self.layout().addRow(
            self.fields['port'].label, self.fields['port'].widget)
        self.fields['database'] = TextField(
            _("Database"), data.get('oerplib', {}).get('database', ''))
        self.layout().addRow(
            self.fields['database'].label, self.fields['database'].widget)
        self.fields['user'] = TextField(
            _("User"), data.get('oerplib', {}).get('user', ''))
        self.layout().addRow(
            self.fields['user'].label, self.fields['user'].widget)
        self.fields['passwd'] = PasswordField(
            _("Password"), data.get('oerplib', {}).get('passwd', ''))
        self.layout().addRow(
            self.fields['passwd'].label, self.fields['passwd'].widget)
        # Buttons
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            parent=self)
        self.layout().addWidget(buttons)
        # Default focus
        self.fields['name'].widget.setFocus()
        # Responses
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def accept(self):
        """Overridden method to save user input."""
        self.data.update({
            'name': self.fields['name'].result,
            'group_id': self.fields['group'].result[1],
            })
        self.data['oerplib'].update({
            'server': self.fields['server'].result,
            'protocol': self.fields['protocol'].result[1],
            'port': self.fields['port'].result,
            'database': self.fields['database'].result,
            'user': self.fields['user'].result,
            'passwd': self.fields['passwd'].result,
            })
        if self.id_:
            Controller['server'].update(self.id_, self.data)
        else:
            Controller['server'].create(self.data)
        QtGui.QDialog.accept(self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
