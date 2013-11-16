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
from PySide.QtCore import QObject, Signal

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.utils.form import FormDialog, TextField, IntField, SelectField

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


class ServerControler(QObject):
    """Server controler."""
    created = Signal(str)
    updated = Signal(str)
    deleted = Signal(str)

    def __init__(self, app):
        QObject.__init__(self)
        self.app = app

    def _clean_form_data(self, data):
        data['group_id'] = data['group'][1]
        data['oerplib'] = {
            'server': data['server'],
            'port': data['port'],
            'database': data['database'],
            'user': data['user'],
            'passwd': data['passwd'],
        }
        del data['group']
        del data['server']
        del data['port']
        del data['database']
        del data['user']
        del data['passwd']
        return data

    def display_form(self, id_=None):
        """Display the form to create/update a server."""
        db_data = id_ and self.read(id_) or copy.deepcopy(DEFAULT)
        groups = self.app.group_ctl.read_all()
        fields = [
            ('name', TextField(_("Name"), db_data.get('name', ''))),
            ('group', SelectField(
                _("Group"),
                [(group['name'], gid) for gid, group in groups.iteritems()],
                list(groups)[0])),
            ('server',
                TextField(_("Host"), db_data['oerplib'].get('server', ''))),
            ('port', IntField(
                _("Port"),
                db_data['oerplib'].get('port', 8069),
                range_=(1, 65535))),
            ('database', TextField(
                _("Database"), db_data['oerplib'].get('database', ''))),
            ('user', TextField(
                _("User"), db_data['oerplib'].get('user', ''))),
            ('passwd', TextField(
                _("Password"), db_data['oerplib'].get('passwd', ''))),
        ]
        new_data, ok = FormDialog(fields).exec_()
        if ok:
            new_data = self._clean_form_data(new_data)
            if id_:
                self.update(id_, new_data)
            else:
                self.create(new_data)
        return ok

    def create(self, data):
        """Create a new server and return its ID."""
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
        """Return data related to a server."""
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
        """Return all servers data."""
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
        """Update a server."""
        # OERPLib credentials
        oerplib.tools.session.save(
            id_, data['oerplib'], rc_file=db.OERPLIB_FILE)
        del data['oerplib']
        # Application specific data
        del data['group_id']
        db_data = db.read()
        for gdata in db_data.itervalues():
            if id_ in gdata['servers']:
                gdata['servers'][id_].update(data)
                db.write(db_data)
                self.updated.emit(id_)
                break

    def delete(self, id_):
        """Delete a server."""
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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
