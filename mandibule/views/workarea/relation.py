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
from mandibule.views.widgets.fields import TextField, IntField
from mandibule.views.workarea.content import GraphFormLayout, GraphContent


class RelationFormLayout(GraphFormLayout):
    """Describe the form for a models relations graph."""

    def init_fields(self, data):
        self.fields['name'] = TextField(_("Name"), data.get('name', ''))
        self.addRow(
            self.fields['name'].label, self.fields['name'].widget)
        self.fields['models'] = TextField(
            _("Starting models"), data.get('models', ''))
        self.addRow(
            self.fields['models'].label, self.fields['models'].widget)
        self.fields['maxdepth'] = IntField(
            _(u"Max depth"), data.get('maxdepth', 1), range_=(0, 42))
        self.addRow(
            self.fields['maxdepth'].label, self.fields['maxdepth'].widget)
        self.fields['whitelist'] = TextField(
            _("Whitelist"), data.get('whitelist', ''), multi=True)
        self.addRow(
            self.fields['whitelist'].label, self.fields['whitelist'].widget)
        self.fields['blacklist'] = TextField(
            _("Blacklist"), data.get('blacklist', ''), multi=True)
        self.addRow(
            self.fields['blacklist'].label, self.fields['blacklist'].widget)
        self.fields['attrs_whitelist'] = TextField(
            _("Attr. whitelist"), data.get('attrs_whitelist', ''),
            multi=True)
        self.addRow(
            self.fields['attrs_whitelist'].label,
            self.fields['attrs_whitelist'].widget)
        self.fields['attrs_blacklist'] = TextField(
            _("Attr. blacklist"), data.get('attrs_blacklist', ''),
            multi=True)
        self.addRow(
            self.fields['attrs_blacklist'].label,
            self.fields['attrs_blacklist'].widget)

    def get_data(self):
        """Return user input data."""
        return {
            'server_id': self.content.server_id,
            'name': self.fields['name'].result,
            'models': self.fields['models'].result,
            'maxdepth': self.fields['maxdepth'].result,
            'whitelist': self.fields['whitelist'].result,
            'blacklist': self.fields['blacklist'].result,
            'attrs_whitelist': self.fields['attrs_whitelist'].result,
            'attrs_blacklist': self.fields['attrs_blacklist'].result,
        }


class RelationContent(GraphContent):
    """Relations graph content."""

    def __init__(self, app, server_id, id_=None, new=False):
        ctl = app.relation_ctl
        GraphContent.__init__(self, app, ctl, server_id, id_, new)
        form = RelationFormLayout(self, id_)
        self.set_form(form)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
