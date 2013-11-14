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

from PySide.QtCore import QObject, Signal

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.utils.form import FormDialog, TextField


class GroupControler(QObject):
    """Group controler."""
    created = Signal(str)
    updated = Signal(str)
    deleted = Signal(str)

    def __init__(self, app):
        QObject.__init__(self)
        self.app = app

    def display_form(self, id_=None):
        """Display the form to create/update a group."""
        data = self.read(id_) or {}
        fields = [
            ('name', TextField(_("Name"), data.get('name', ''))),
        ]
        new_data, ok = FormDialog(fields).exec_()
        if ok:
            if id_:
                self.update(id_, new_data)
            else:
                self.create(new_data)
        return ok

    def create(self, data):
        """Create a new group and return its ID."""
        id_ = uuid.uuid4().hex
        data['servers'] = []
        db_data = db.read()
        db_data[id_] = data
        db.write(db_data)
        self.created.emit(id_)
        return id_

    def read(self, id_):
        """Return data related to a group."""
        db_data = db.read()
        if id_ in db_data:
            # We remove servers from data returned
            del db_data[id_]['servers']
            return db_data[id_]
        return None

    def read_all(self):
        db_data = db.read()
        for id_ in db_data:
            del db_data[id_]['servers']
        return db_data

    def update(self, id_, data):
        """Update a group."""
        db_data = db.read()
        if id_ in db_data:
            db_data[id_].update(data)
            db.write(db_data)
            self.updated.emit(id_)

    def delete(self, id_):
        """Delete a group."""
        # TODO confirmation via popup
        db_data = db.read()
        if id_ in db_data:
            if 'servers' in db_data[id_]:
                raise ValueError(
                    _("Unable to delete this group while it contains servers."))
            del db_data[id_]
            db.write(db_data)
            self.deleted.emit(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
