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

from PySide import QtGui

from mandibule.utils.i18n import _
from mandibule.views.widgets.fields import TextField, IntField


class RelationForm(QtGui.QDialog):
    """Relational graph form."""
    def __init__(self, app, id_=None, data=None):
        QtGui.QDialog.__init__(self)
        self.app = app
        self.id_ = id_
        self.data = data
        self.fields = {}
        self.setLayout(QtGui.QFormLayout())
        # Fields
        self.fields['name'] = TextField(_("Name"), data.get('name', ''))
        self.layout().addRow(
            self.fields['name'].label, self.fields['name'].widget)
        self.fields['models'] = TextField(
            _("Starting models"), data.get('models', ''))
        self.layout().addRow(
            self.fields['models'].label, self.fields['models'].widget)
        self.fields['maxdepth'] = IntField(
            _(u"Max depth"), data.get('maxdepth', 1), range_=(0, 42))
        self.layout().addRow(
            self.fields['maxdepth'].label, self.fields['maxdepth'].widget)
        self.fields['whitelist'] = TextField(
            _("Whitelist"), data.get('whitelist', ''), multi=True)
        self.layout().addRow(
            self.fields['whitelist'].label, self.fields['whitelist'].widget)
        self.fields['blacklist'] = TextField(
            _("Blacklist"), data.get('blacklist', ''), multi=True)
        self.layout().addRow(
            self.fields['blacklist'].label, self.fields['blacklist'].widget)
        self.fields['attrs_whitelist'] = TextField(
            _("Attr. whitelist"), data.get('attrs_whitelist', ''), multi=True)
        self.layout().addRow(
            self.fields['attrs_whitelist'].label,
            self.fields['attrs_whitelist'].widget)
        self.fields['attrs_blacklist'] = TextField(
            _("Attr. blacklist"), data.get('attrs_blacklist', ''), multi=True)
        self.layout().addRow(
            self.fields['attrs_blacklist'].label,
            self.fields['attrs_blacklist'].widget)
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
            'models': self.fields['models'].result,
            'maxdepth': self.fields['maxdepth'].result,
            'whitelist': self.fields['whitelist'].result,
            'blacklist': self.fields['blacklist'].result,
            'attrs_whitelist': self.fields['attrs_whitelist'].result,
            'attrs_blacklist': self.fields['attrs_blacklist'].result,
            })
        if self.id_:
            self.app.relation_ctl.update(self.id_, self.data)
        else:
            self.app.relation_ctl.create(self.data)
        QtGui.QDialog.accept(self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
