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
from mandibule.views.widgets.fields import TextField, BoolField


class DependencyForm(QtGui.QDialog):
    """Module dependencies graph form."""
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
        self.fields['modules'] = TextField(
            _("Starting modules"), data.get('modules', ''))
        self.layout().addRow(
            self.fields['modules'].label, self.fields['modules'].widget)
        self.fields['models'] = TextField(
            _("Models"), data.get('models', ''), multi=True)
        self.layout().addRow(
            self.fields['models'].label,
            self.fields['models'].widget)
        self.fields['models_blacklist'] = TextField(
            _("Models blacklist"), data.get('models_blacklist', ''), multi=True)
        self.layout().addRow(
            self.fields['models_blacklist'].label,
            self.fields['models_blacklist'].widget)
        self.fields['restrict'] = BoolField(
            _("Restrict to models"), data.get('restrict', False))
        self.layout().addRow(
            self.fields['restrict'].label,
            self.fields['restrict'].widget)
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
            'modules': self.fields['modules'].result,
            'models': self.fields['models'].result,
            'models_blacklist': self.fields['models_blacklist'].result,
            'restrict': self.fields['restrict'].result,
            })
        if self.id_:
            self.app.dependency_ctl.update(self.id_, self.data)
        else:
            self.app.dependency_ctl.create(self.data)
        QtGui.QDialog.accept(self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
