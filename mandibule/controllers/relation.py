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

from PySide.QtCore import QObject, QThreadPool, Signal

import oerplib

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.widgets.form import FormDialog, TextField, IntField
from mandibule.controllers import GraphWorker

DEFAULT = {
    'name': '', 
    'attrs_blacklist': '',
    'models': '', 
    'whitelist': '*', 
    'blacklist': '', 
    'attrs_whitelist': '*', 
    'maxdepth': 1,
}


class RelationController(QObject):
    """Relational graph function controller."""
    created = Signal(str)
    updated = Signal(str)
    deleted = Signal(str)
    executed = Signal(str, str)
    execute_error = Signal(str)
    finished = Signal(str, tuple)

    def __init__(self, app):
        QObject.__init__(self)
        self.app = app

    def display_form(self, id_=None, server_id=None):
        """Display the form to create/update a relation graph."""
        db_data = id_ and self.read(id_) or copy.deepcopy(DEFAULT)
        fields = [
            ('name', TextField(_("Name"), db_data.get('name', ''))),
            ('models', TextField(
                u"%s\n(e.g. 'res.partner sale.order')" % (
                    _(u"Starting models")),
                db_data.get('models', ''))),
            ('maxdepth', IntField(
                _(u"Max depth"), db_data.get('maxdepth', 1), range_=(1, 10))),
            ('whitelist', TextField(
                u"%s\n(e.g. 'sale.* product.product')" % (_(u"Whitelist")),
                db_data.get('whitelist', ''), multi=True)),
            ('blacklist', TextField(
                u"%s\n(e.g. 'res.users')" % (_(u"Blacklist")),
                db_data.get('blacklist', ''), multi=True)),
            ('attrs_whitelist', TextField(
                u"%s\n(models to display with attributes)" % (
                    _(u"Attrs whitelist")),
                db_data.get('attrs_whitelist', ''),
                multi=True)),
            ('attrs_blacklist', TextField(
                _(u"Attrs black list"),
                db_data.get('attrs_blacklist', ''),
                multi=True)),
        ]
        new_data, ok = FormDialog(fields).exec_()
        if ok:
            new_data['server_id'] = server_id or db_data['server_id']
            if id_:
                self.update(id_, new_data)
            else:
                self.create(new_data)
        return ok

    def create(self, data):
        """Create a new relational graph and return its ID."""
        id_ = uuid.uuid4().hex
        db_data = db.read()
        sid = data['server_id']
        gid = self.app.server_ctl.read(sid)['group_id']
        if 'relations' not in db_data[gid]['servers'][sid]:
            db_data[gid]['servers'][sid]['relations'] = {}
        db_data[gid]['servers'][sid]['relations'][id_] = data
        db.write(db_data)
        self.created.emit(id_)
        return id_

    def read(self, id_):
        """Return data related to a relational graph."""
        db_data = db.read()
        for gdata in db_data.itervalues():
            for sid, sdata in gdata['servers'].iteritems():
                if id_ in sdata.get('relations', {}):
                    rdata = sdata['relations'][id_]
                    rdata['server_id'] = sid
                    return rdata
        return None

    def read_all(self):
        """Return all relational graph data."""
        db_data = db.read()
        data = {}
        for gdata in db_data.itervalues():
            for sid, sdata in gdata['servers'].iteritems():
                for rid, rdata in sdata.get('relations', {}).iteritems():
                    data[rid] = rdata
                    data[rid]['server_id'] = sid
        return data

    def update(self, id_, data):
        """Update a relationl graph."""
        del data['server_id']
        db_data = db.read()
        for gdata in db_data.itervalues():
            for sdata in gdata['servers'].itervalues():
                if id_ in sdata.get('relations', {}):
                    sdata['relations'][id_].update(data)
                    db.write(db_data)
                    self.updated.emit(id_)
                    return

    def delete(self, id_):
        """Delete a relational graph."""
        db_data = db.read()
        for gdata in db_data.itervalues():
            for sdata in gdata['servers'].itervalues():
                if id_ in sdata.get('relations', {}):
                    del sdata['relations'][id_]
                    db.write(db_data)
                    self.deleted.emit(id_)
                    return

    def execute(self, id_):
        """Generate the relation graph."""
        self.executed.emit(id_, "Working...")
        worker = GraphWorker(id_, lambda: self._execute(id_))
        worker.result_ready.connect(self._process_result)
        worker.exception_raised.connect(self._handle_exception)
        QThreadPool.globalInstance().start(worker)

    def _execute(self, id_):
        """Internal threaded method requesting the result."""
        data = self.read(id_)
        oerp = oerplib.OERP.load(data['server_id'], rc_file=db.OERPLIB_FILE)
        graph = oerp.inspect.relations(
            [str(model) for model in data['models'].split()],
            data['maxdepth'],
            [str(model) for model in data['whitelist'].split()],
            [str(model) for model in data['blacklist'].split()],
            [str(model) for model in data['attrs_whitelist'].split()],
            [str(model) for model in data['attrs_blacklist'].split()])
        return graph.make_dot().create_png()

    def _process_result(self, id_, result):
        """Slot which emit the 'finished' signal to views."""
        self.finished.emit(id_, result)

    def _handle_exception(self, id_, message):
        """Slot performed if the threaded method has raised an exception."""
        self.execute_error.emit(id_)
        raise RuntimeError(message)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
