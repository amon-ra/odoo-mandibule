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

from PySide import QtCore, QtGui

from mandibule.utils.i18n import _
from mandibule.views.widgets.zoomableimage import ZoomableImage


class Content(QtGui.QWidget):
    """Base class to represent and manage the content of a function."""
    def __init__(self, app, ctl, id_):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.ctl = ctl
        self.id_ = id_
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.setEnabled(False)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

    def set_data(self, data):
        """Update data of the content."""
        pass


class GraphContent(Content):
    """Base class to represent and manage the content of a graph function."""
    def __init__(self, app, ctl, id_):
        super(GraphContent, self).__init__(app, ctl, id_)
        self._image = ZoomableImage()
        self._image.setEnabled(False)
        self.layout().addWidget(self._image)
        # Connect to the controller
        #self.ctl.updated.connect(self.updated)
        self.ctl.executed.connect(self.executed)
        self.ctl.execute_error.connect(self.execute_error)
        self.ctl.finished.connect(self.finished)
        self._actions = {}
        # Edit parameters
        self._actions['edit'] = QtGui.QAction(
            self.app.icons.icon_edit, _(u"Edit parameters"), self)
        self._actions['edit'].setShortcut('Ctrl+E')
        self._actions['edit'].triggered.connect(
            lambda: self.ctl.display_form(self.id_))
        self.toolbar.addAction(self._actions['edit'])
        self.toolbar.addSeparator()
        # Execute
        self._actions['execute'] = QtGui.QAction(
            self.app.icons.icon_exe, _(u"Execute"), self)
        self._actions['execute'].setShortcut('Ctrl+X')
        self._actions['execute'].triggered.connect(
            lambda: self.ctl.execute(self.id_))
        self.toolbar.addAction(self._actions['execute'])
        self.toolbar.addSeparator()
        # Zoom in
        self._actions['zoom_in'] = QtGui.QAction(
            self.app.icons.icon_zoom_in, _(u"Zoom in"), self)
        self._actions['zoom_in'].setShortcut('Ctrl++')
        self._actions['zoom_in'].triggered.connect(self._image.zoom_in)
        self.toolbar.addAction(self._actions['zoom_in'])
        # Zoom out
        self._actions['zoom_out'] = QtGui.QAction(
            self.app.icons.icon_zoom_out, _(u"Zoom out"), self)
        self._actions['zoom_out'].setShortcut('Ctrl+-')
        self._actions['zoom_out'].triggered.connect(self._image.zoom_out)
        self.toolbar.addAction(self._actions['zoom_out'])
        # Zoom original
        self._actions['zoom_orig'] = QtGui.QAction(
            self.app.icons.icon_zoom_orig, _(u"Original size"), self)
        self._actions['zoom_orig'].setShortcut('Ctrl+0')
        self._actions['zoom_orig'].triggered.connect(self._image.zoom_original)
        self.toolbar.addAction(self._actions['zoom_orig'])
        # Zoom fit best
        self._actions['zoom_fit_best'] = QtGui.QAction(
            self.app.icons.icon_zoom_fit, _(u"Fit to window"), self)
        self._actions['zoom_fit_best'].setShortcut('Ctrl+=')
        self._actions['zoom_fit_best'].triggered.connect(
            self._image.zoom_fit_best)
        self.toolbar.addAction(self._actions['zoom_fit_best'])

    def set_data(self, data):
        self._image.update_image(data)

    def executed(self, id_):
        """Update the content when the function is executed."""
        if id_ == self.id_:
            self.toolbar.setEnabled(False)
            self._image.setEnabled(False)

    def execute_error(self, id_):
        if id_ == self.id_:
            # TODO
            pass

    def finished(self, id_, data):
        """Update the content with `data` when the function is finished."""
        if id_ == self.id_:
            self.set_data(data[0])
            self.toolbar.setEnabled(True)
            self._image.zoom_fit_best()
            self._image.setEnabled(True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
