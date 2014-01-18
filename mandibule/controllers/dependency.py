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

from PySide.QtCore import QThreadPool, Signal

import oerplib

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.controllers import Controller
from mandibule.views.widgets.dialog import confirm
from mandibule.controllers import GraphWorker


class DependencyController(Controller):
    """Module dependencies graph function controller."""
    created = Signal(str, dict, dict)
    updated = Signal(str, dict, dict)
    deleted = Signal(str, dict)
    executed = Signal(str, dict, dict)
    execute_error = Signal(str, dict)
    finished = Signal(str, tuple, dict)

    def default_get(self, default=None, context=None):
        """Return default data values."""
        if context is None:
            context = {}
        if default is None:
            default = {}
        context['model'] = 'dependency'
        data = {
            'name': '',
            'modules': '',
            'models': '',
            'models_blacklist': '',
            'restrict': False,
        }
        data.update(default)
        return data

    def display_form(self, id_=None, data=None, context=None):
        """Display a form to create/edit an existing record. If `id_` is None,
        no data will be saved (live-edit on the view). Default values of the
        form can be set through the `data` dictionary.
        """
        if context is None:
            context = {}
        context['model'] = 'dependency'
        if id_:
            self.app.work_area.edit_function(id_, context)
        else:
            self.app.work_area.new_function(
                self.app.actions.get_server_id(), context)

    def create(self, data, context=None):
        """Create a new record from `data` and return its ID."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        id_ = uuid.uuid4().hex
        db_data = db.read()
        data_copy = data.copy()
        sid = data_copy.pop('server_id')
        gid = self.app.server_ctl.read(sid)['group_id']
        if 'dependencies' not in db_data[gid]['servers'][sid]:
            db_data[gid]['servers'][sid]['dependencies'] = {}
        db_data[gid]['servers'][sid]['dependencies'][id_] = data_copy
        db.write(db_data)
        self.created.emit(id_, data, context)
        return id_

    def read(self, id_, context=None):
        """Return data related to the record identified by `id_`."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        db_data = db.read()
        for gdata in db_data.itervalues():
            for sid, sdata in gdata['servers'].iteritems():
                if id_ in sdata.get('dependencies', {}):
                    rdata = sdata['dependencies'][id_]
                    rdata['server_id'] = sid
                    return rdata
        return None

    def read_all(self, context=None):
        """Return all records data."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        db_data = db.read()
        data = {}
        for gdata in db_data.itervalues():
            for sid, sdata in gdata['servers'].iteritems():
                for rid, rdata in sdata.get('dependencies', {}).iteritems():
                    data[rid] = rdata
                    data[rid]['server_id'] = sid
        return data

    def update(self, id_, data, context=None):
        """Update a record identified by `id_` with `data`."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        data_copy = data.copy()
        data_copy.pop('server_id')
        db_data = db.read()
        for gdata in db_data.itervalues():
            for sdata in gdata['servers'].itervalues():
                if id_ in sdata.get('dependencies', {}):
                    sdata['dependencies'][id_].update(data_copy)
                    db.write(db_data)
                    self.updated.emit(id_, data, context)
                    return

    def delete(self, id_, context=None):
        """Delete a record identified by `id_`."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        db_data = db.read()
        for gdata in db_data.itervalues():
            for sdata in gdata['servers'].itervalues():
                if id_ in sdata.get('dependencies', {}):
                    del sdata['dependencies'][id_]
                    db.write(db_data)
                    self.deleted.emit(id_, context)
                    return

    def delete_confirm(self, id_, context=None):
        """Display a confirmation dialog to the user before delete."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        data = self.read(id_)
        response = confirm(
            self.app.main_window,
            _(u"Are you sure you want to delete the function "
              u"<strong>%s</strong>?") % (data['name']))
        if response:
            self.delete(id_)

    def execute(self, id_, data=None, context=None):
        """Generate the relation graph."""
        if context is None:
            context = {}
        context['model'] = 'dependency'
        if not data:
            data = self.read(id_)
        self.executed.emit(id_, data, context)
        worker = GraphWorker(id_, lambda: self._execute(id_, data), context)
        worker.result_ready.connect(self._process_result)
        worker.exception_raised.connect(self._handle_exception)
        QThreadPool.globalInstance().start(worker)

    def _execute(self, id_, data):
        """Internal threaded method requesting the result."""
        oerp = oerplib.OERP.load(data['server_id'], rc_file=db.OERPLIB_FILE)
        graph = oerp.inspect.dependencies(
            [str(model) for model in data['modules'].split()],
            [str(model) for model in data['models'].split()],
            [str(model) for model in data['models_blacklist'].split()],
            data['restrict'])
        return graph.make_dot().create_png()

    def _process_result(self, id_, result, context):
        """Slot which emit the 'finished' signal to views."""
        self.finished.emit(id_, result, context)

    def _handle_exception(self, id_, message, context):
        """Slot performed if the threaded method has raised an exception."""
        self.execute_error.emit(id_, context)
        raise RuntimeError(message)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
