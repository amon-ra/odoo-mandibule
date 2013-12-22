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

__all__ = ['GroupController', 'ServerController',
           'RelationController', 'DependencyController']

from PySide.QtCore import QObject, QRunnable, Signal


class GraphWorker(QObject, QRunnable):
    """Working thread which has for result a graph/image."""
    result_ready = Signal(str, tuple)
    exception_raised = Signal(str, str)

    def __init__(self, id_, function):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.id = id_
        self._function = function

    def run(self):
        try:
            result = self._function()
        except Exception as exc:
            message = getattr(exc, 'message') or getattr(exc, 'strerror')
            if type(message) == str:
                message = message.decode('utf-8')
            self.exception_raised.emit(self.id, message)
        else:
            # HACK: Pass the image in a tuple, otherwise the 'result' is
            # copied by Qt # making it unusable
            self.result_ready.emit(self.id, (result,))


class Controller(QObject):
    """Base controller which defines common methods."""

    def __init__(self, app):
        QObject.__init__(self)
        self.app = app

    def display_form(self, id_=None, data=None):
        """Display a form to create/edit an existing record. If `id_` is None,
        no data will be saved (live-edit on the view). Default values of the
        form can be set through the `data` dictionary.
        """
        raise NotImplementedError

    def create(self, data):
        """Create a new record from `data` and return its ID."""
        raise NotImplementedError

    def read(self, id_):
        """Return data related to the record identified by `id_`."""
        raise NotImplementedError

    def read_all(self):
        """Return all records data."""
        raise NotImplementedError

    def update(self, id_, data):
        """Update a record identified by `id_` with `data`."""
        raise NotImplementedError

    def delete(self, id_):
        """Delete a record identified by `id_`."""
        raise NotImplementedError

    def delete_confirm(self, id_):
        """Display a confirmation dialog to the user before delete."""
        raise NotImplementedError


from mandibule.controllers.group import GroupController
from mandibule.controllers.server import ServerController
from mandibule.controllers.relation import RelationController
from mandibule.controllers.dependency import DependencyController

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
