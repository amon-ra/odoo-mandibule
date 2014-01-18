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
from mandibule.utils.i18n import _
from mandibule.views.widgets.fields import TextField, BoolField
from mandibule.views.workarea.content import GraphFormLayout, GraphContent


class DependencyFormLayout(GraphFormLayout):
    """Describe the form for a modules dependencies graph."""

    def init_fields(self, data):
        self.fields['name'] = TextField(_("Name"), data.get('name', ''))
        self.addRow(
            self.fields['name'].label,
            self.fields['name'].widget)
        self.fields['modules'] = TextField(
            _("Starting modules"), data.get('modules', ''))
        self.addRow(
            self.fields['modules'].label,
            self.fields['modules'].widget)
        self.fields['models'] = TextField(
            _("Models"), data.get('models', ''), multi=True)
        self.addRow(
            self.fields['models'].label,
            self.fields['models'].widget)
        self.fields['models_blacklist'] = TextField(
            _("Models blacklist"), data.get('models_blacklist', ''), multi=True)
        self.addRow(
            self.fields['models_blacklist'].label,
            self.fields['models_blacklist'].widget)
        self.fields['restrict'] = BoolField(
            _("Restrict to models"), data.get('restrict', False))
        self.addRow(
            self.fields['restrict'].label,
            self.fields['restrict'].widget)

    def get_data(self):
        """Return user input data."""
        return {
            'server_id': self.content.server_id,
            'name': self.fields['name'].result,
            'modules': self.fields['modules'].result,
            'models': self.fields['models'].result,
            'models_blacklist': self.fields['models_blacklist'].result,
            'restrict': self.fields['restrict'].result,
        }


class DependencyContent(GraphContent):
    """Dependencies graph content."""

    def __init__(self, app, server_id, id_=None, new=False):
        ctl = app.dependency_ctl
        GraphContent.__init__(self, app, ctl, server_id, id_, new)
        form = DependencyFormLayout(self, id_)
        self.set_form(form)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
