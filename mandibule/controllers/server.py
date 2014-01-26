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

import oerplib
from PySide.QtCore import Signal

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.controllers import Controller
from mandibule.views.widgets.dialog import confirm
from mandibule.views.forms import ServerForm

DEFAULT = {
    'name': '',
    'oerplib': {
        'type': 'OERP',
        'server': 'localhost',
        'protocol': 'xmlrpc',
        'port': 8069,
        'database': '',
        'user': 'admin',
        'passwd': '',
        'timeout': 120,
    },
}


class ServerController(Controller):
    """Server controller."""
    created = Signal(str)
    updated = Signal(str)
    deleted = Signal(str)
    group_changed = Signal(str, str, str)

    def display_form(self, id_=None, data=None):
        """Display a form to create/edit an existing record. If `id_` is None,
        no data will be saved (live-edit on the view). Default values of the
        form can be set through the `data` dictionary.
        """
        data = data or (id_ and self.read(id_)) or copy.deepcopy(DEFAULT)
        ServerForm(self.app, id_, data).exec_()

    def create(self, data):
        """Create a new record from `data` and return its ID."""
        id_ = uuid.uuid4().hex
        # OERPLib credentials
        oerplib.tools.session.save(
            id_, data['oerplib'], rc_file=db.OERPLIB_FILE)
        del data['oerplib']
        # Application specific data
        db_data = db.read()
        gid = data['group_id']
        db_data[gid]['servers'][id_] = data
        db.write(db_data)
        self.created.emit(id_)
        return id_

    def read(self, id_):
        """Return data related to the record identified by `id_`."""
        db_data = db.read()
        oe_data = oerplib.tools.session.get(id_, rc_file=db.OERPLIB_FILE)
        for gid, gdata in db_data.iteritems():
            if id_ in gdata['servers']:
                sdata = gdata['servers'][id_]
                sdata['oerplib'] = oe_data
                sdata['group_id'] = gid
                return sdata
        return None

    def read_all(self):
        """Return all records data."""
        db_data = db.read()
        data = {}
        for gid, gdata in db_data.iteritems():
            for sid, sdata in gdata['servers'].iteritems():
                oe_data = oerplib.tools.session.get(
                    sid, rc_file=db.OERPLIB_FILE)
                data[sid] = sdata
                data[sid]['oerplib'] = oe_data
                data[sid]['group_id'] = gid
        return data

    def update(self, id_, data):
        """Update a record identified by `id_` with `data`."""
        # OERPLib credentials
        oerplib.tools.session.save(
            id_, data['oerplib'], rc_file=db.OERPLIB_FILE)
        del data['oerplib']
        # Application specific data
        new_gid =  data.pop('group_id')
        db_data = db.read()
        for gid, gdata in db_data.iteritems():
            if id_ in gdata['servers']:
                # If the server group has not changed, update it in place
                if gid == new_gid:
                    gdata['servers'][id_].update(data)
                # Otherwise, remove the server from its old group, and add it
                # to the new one
                else:
                    gdata['servers'].pop(id_)
                    db_data[new_gid]['servers'][id_] = data
                break
        # Update the data
        db.write(db_data)
        self.updated.emit(id_)
        # Signal if the group has changed
        if gid != new_gid:
            self.group_changed.emit(id_, gid, new_gid)

    def delete(self, id_):
        """Delete a record identified by `id_`."""
        # OERPLib credentials
        oerplib.tools.session.remove(id_, rc_file=db.OERPLIB_FILE)
        # Application specific data
        db_data = db.read()
        for gdata in db_data.itervalues():
            if id_ in gdata['servers']:
                del gdata['servers'][id_]
                db.write(db_data)
                self.deleted.emit(id_)
                break

    def delete_confirm(self, id_):
        """Display a confirmation dialog to the user before delete."""
        data = self.read(id_)
        response = confirm(
            self.app.main_window,
            _(u"Are you sure you want to delete the server "
              u"<strong>%s</strong>?") % (data['name']))
        if response:
            self.delete(id_)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
