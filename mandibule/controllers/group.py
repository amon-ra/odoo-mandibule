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
import uuid
import copy

from PySide.QtCore import Signal

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.controllers import Controller
from mandibule.views.widgets.dialog import confirm
from mandibule.views.forms import GroupForm

DEFAULT = {
    'name': '',
}


class GroupController(Controller):
    """Group controller."""
    created = Signal(str)
    updated = Signal(str)
    deleted = Signal(str)

    def display_form(self, id_=None, data=None):
        """Display a form to edit an existing record. If `id_` is None, no
        data will be saved (live-edit on the view). Default values of the form
        can be set through the `data` dictionary.
        """
        data = data or (id_ and self.read(id_)) or copy.deepcopy(DEFAULT)
        GroupForm(self.app, id_, data).exec_()

    def create(self, data):
        """Create a new record from `data` and return its ID."""
        id_ = uuid.uuid4().hex
        data['servers'] = {}
        db_data = db.read()
        db_data[id_] = data
        db.write(db_data)
        self.created.emit(id_)
        return id_

    def read(self, id_):
        """Return data related to the record identified by `id_`."""
        db_data = db.read()
        if id_ in db_data:
            # We remove servers from data returned
            #del db_data[id_]['servers']
            return db_data[id_]
        return None

    def read_all(self):
        """Return all records data."""
        db_data = db.read()
        #for id_ in db_data:
        #    del db_data[id_]['servers']
        return db_data

    def update(self, id_, data):
        """Update a record identified by `id_` with `data`."""
        db_data = db.read()
        if id_ in db_data:
            db_data[id_].update(data)
            db.write(db_data)
            self.updated.emit(id_)

    def delete(self, id_):
        """Delete a record identified by `id_`."""
        db_data = db.read()
        if id_ in db_data:
            if db_data[id_].get('servers'):
                raise Warning(
                    _(u"Unable to delete a group while it contains servers."))
            del db_data[id_]
            db.write(db_data)
            self.deleted.emit(id_)

    def delete_confirm(self, id_):
        """Display a confirmation dialog to the user before delete."""
        data = self.read(id_)
        response = confirm(
            self.app.main_window,
            _(u"Are you sure you want to delete the group "
              u"<strong>%s</strong>?") % (data['name']))
        if response:
            self.delete(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
