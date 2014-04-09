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
"""Common tools used to generate a graph."""
from PySide import QtCore, QtGui

from mandibule.reg import Icons, WorkArea, Controller
from mandibule.utils.i18n import _
from mandibule.widgets.zoomableimage import ZoomableImage


class GraphWorker(QtCore.QObject, QtCore.QRunnable):
    """Working thread which has for result a graph/image."""
    result_ready = QtCore.Signal(str, tuple)
    exception_raised = QtCore.Signal(str, str)

    def __init__(self, id_, function):
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self)
        self.id_ = id_
        self._function = function

    def run(self):
        try:
            graph = self._function()
        except Exception as exc:
            message = getattr(exc, 'message') or getattr(exc, 'strerror')
            if type(message) == str:
                message = message.decode('utf-8')
            self.exception_raised.emit(self.id_, message)
        else:
            self.result_ready.emit(self.id_, graph)


class GraphPanel(QtGui.QScrollArea):
    """Panel used inside a `GraphWorkArea`."""
    hidden = QtCore.Signal(bool)

    def __init__(self, workarea, parent=None, layout=None):
        QtGui.QScrollArea.__init__(self, parent)
        self.workarea = workarea
        self.setFrameStyle(QtGui.QFrame.WinPanel | QtGui.QFrame.Plain)
        if layout:
            self.setLayout(layout)
        self.hide()

    def setLayout(self, layout):
        """Set the workarea of the panel."""
        QtGui.QScrollArea.setLayout(self, layout)
        self.resize(
            self.layout().minimumSize().width(),
            self.layout().minimumSize().height())

    def hide(self):
        """Emit the 'hidden' with `True` once the panel is hidden."""
        QtGui.QScrollArea.hide(self)
        self.hidden.emit(True)

    def show(self):
        """Emit the 'hidden' with `False` once the panel is displayed."""
        QtGui.QScrollArea.show(self)
        self.hidden.emit(False)

    def get_data(self):
        return self.layout().get_data()


class GraphFormLayout(QtGui.QFormLayout):
    """Describe the form inserted in a `GraphPanel`."""
    data_changed = QtCore.Signal()
    data_restored = QtCore.Signal()

    def __init__(self, workarea, id_=None):
        QtGui.QFormLayout.__init__(self)
        self.workarea = workarea
        ctl = self.workarea.ctl
        data = id_ and ctl.read(id_) \
            or ctl.default_get({'server_id': workarea.server_id})
        # Fields
        self.fields = {}
        self.init_fields(data)
        # Buttons
        self.button_save = QtGui.QPushButton(Icons['save'], _(u"Save"))
        self.button_save.clicked.connect(self.workarea.save)
        self.button_save.setEnabled(self.workarea.unsaved)
        self.button_restore = QtGui.QPushButton(Icons['undo'], _(u"Undo"))
        self.button_restore.clicked.connect(self.workarea.restore)
        self.button_restore.setEnabled(False)
        self.button_close = QtGui.QPushButton(Icons['ok'], _(u"Close"))
        self.button_close.clicked.connect(
            lambda: self.workarea.show_panel(False))
        self.button_execute = QtGui.QPushButton(Icons['exe'], _(u"Execute"))
        self.button_execute.clicked.connect(self.workarea.execute)
        self.buttons_box = QtGui.QHBoxLayout()
        self.buttons_box.addWidget(self.button_save)
        self.buttons_box.addWidget(self.button_restore)
        self.buttons_box.addWidget(self.button_close)
        self.buttons_box.addWidget(self.button_execute)
        self.addRow(self.buttons_box)
        # Default focus
        self.fields['name'].widget.setFocus()
        # Connect signals
        for field in self.fields.itervalues():
            field.changed.connect(self.data_changed.emit)
            field.changed.connect(self._function_unsaved)
        ctl.created.connect(self._function_saved)
        ctl.updated.connect(self._function_saved)
        ctl.deleted.connect(self._function_unsaved)
        self.data_restored.connect(self._function_restored)

    def init_fields(self, data):
        """Prepare and insert fields in the form."""
        raise NotImplementedError

    def get_data(self):
        """Return user input data."""
        raise NotImplementedError

    def set_data(self, data):
        """Inject `data` in the form."""
        self.blockSignals(True)
        for field, value in data.iteritems():
            if field in self.fields:
                self.fields[field].set_value(value)
        self.blockSignals(False)
        self.data_restored.emit()

    def _function_saved(self, *args):
        """Disable the save button once the function is saved."""
        self.button_save.setEnabled(False)
        self.button_restore.setEnabled(False)

    def _function_unsaved(self, *args):
        """Enable the save button once the function is deleted."""
        self.button_save.setEnabled(True)
        if not self.workarea.new:
            self.button_restore.setEnabled(True)

    def _function_restored(self, *args):
        """Disable the save button once the function is restored."""
        self.button_save.setEnabled(False)
        self.button_restore.setEnabled(False)


class GraphWorkAreaToolbar(QtGui.QToolBar):
    """Toolbar used inside a `GraphWorkArea`."""

    def __init__(self, workarea):
        QtGui.QToolBar.__init__(self)
        self.workarea = workarea
        self.setIconSize(QtCore.QSize(16, 16))
        self._actions = {}
        # Export
        self._actions['export'] = QtGui.QAction(
            Icons['export'], _(u"Export"), self)
        self._actions['export'].setEnabled(False)
        self._actions['export'].triggered.connect(self.workarea.export)
        self.addAction(self._actions['export'])
        # Save
        self._actions['save'] = QtGui.QAction(
            Icons['save'], _(u"Save"), self)
        self._actions['save'].setShortcut(QtGui.QKeySequence.Save)
        self._actions['save'].setEnabled(False)
        self._actions['save'].triggered.connect(self.workarea.save)
        self.addAction(self._actions['save'])
        # Restore modifications
        self._actions['restore'] = QtGui.QAction(
            Icons['undo'], _(u"Undo modifications"), self)
        self._actions['restore'].setShortcut('Ctrl+U')
        self._actions['restore'].setEnabled(False)
        self._actions['restore'].triggered.connect(self.workarea.restore)
        self.addAction(self._actions['restore'])
        # Edit parameters
        self._actions['edit'] = QtGui.QAction(
            Icons['edit'], _(u"Edit parameters"), self)
        self._actions['edit'].setShortcut('Ctrl+E')
        self._actions['edit'].setCheckable(True)
        self._actions['edit'].toggled.connect(self.workarea.show_panel)
        self.addAction(self._actions['edit'])
        self.addSeparator()
        # Execute
        self._actions['execute'] = QtGui.QAction(
            Icons['exe'], _(u"Execute"), self)
        self._actions['execute'].setShortcut('Ctrl+X')
        self._actions['execute'].triggered.connect(self.workarea.execute)
        self.addAction(self._actions['execute'])
        self.addSeparator()
        # Zoom in
        self._actions['zoom_in'] = QtGui.QAction(
            Icons['zoom_in'], _(u"Zoom in"), self)
        self._actions['zoom_in'].setShortcut(QtGui.QKeySequence.ZoomIn)
        self._actions['zoom_in'].setEnabled(False)
        self._actions['zoom_in'].triggered.connect(
            self.workarea.image.zoom_in)
        self.addAction(self._actions['zoom_in'])
        # Zoom out
        self._actions['zoom_out'] = QtGui.QAction(
            Icons['zoom_out'], _(u"Zoom out"), self)
        self._actions['zoom_out'].setShortcut(QtGui.QKeySequence.ZoomOut)
        self._actions['zoom_out'].setEnabled(False)
        self._actions['zoom_out'].triggered.connect(
            self.workarea.image.zoom_out)
        self.addAction(self._actions['zoom_out'])
        # Zoom original
        self._actions['zoom_orig'] = QtGui.QAction(
            Icons['zoom_orig'], _(u"Original size"), self)
        self._actions['zoom_orig'].setShortcut('Ctrl+0')
        self._actions['zoom_orig'].setEnabled(False)
        self._actions['zoom_orig'].triggered.connect(
            self.workarea.image.zoom_original)
        self.addAction(self._actions['zoom_orig'])
        # Zoom fit best
        self._actions['zoom_fit_best'] = QtGui.QAction(
            Icons['zoom_fit'], _(u"Fit to window"), self)
        self._actions['zoom_fit_best'].setShortcut('Ctrl+=')
        self._actions['zoom_fit_best'].setEnabled(False)
        self._actions['zoom_fit_best'].triggered.connect(
            self.workarea.image.zoom_fit_best)
        self.addAction(self._actions['zoom_fit_best'])

    def toggle_edit_action(self, not_toggled):
        self._actions['edit'].setChecked(not not_toggled)

    def function_saved(self, *args):
        self._actions['save'].setEnabled(False)
        self._actions['restore'].setEnabled(False)

    def function_unsaved(self):
        self._actions['save'].setEnabled(True)
        if not self.workarea.new:
            self._actions['restore'].setEnabled(True)

    def function_restored(self, *args):
        self._actions['save'].setEnabled(False)
        self._actions['restore'].setEnabled(False)

    def function_deleted(self, *args):
        self._actions['save'].setEnabled(True)

    def function_finished(self):
        for action in ['export', 'zoom_in', 'zoom_out',
                       'zoom_orig', 'zoom_fit_best']:
            self._actions[action].setEnabled(True)


class GraphWorkArea(WorkArea):
    """Abstract workarea widget to represent and manage a graph."""
    created = QtCore.Signal(str, str, str)
    data_changed = QtCore.Signal(str, str, dict)
    data_restored = QtCore.Signal(str, str, dict)

    def __init__(self, app, model, server_id, id_=None, new=False):
        WorkArea.__init__(self, app)
        self.app = app
        self._model = model
        self.ctl = Controller[model]
        self.server_id = server_id
        self.id_ = id_
        self.new = new
        self.unsaved = False
        self.graph = None
        # Image and toolbar
        self.image = ZoomableImage()
        self.toolbar = GraphWorkAreaToolbar(self)
        # Place elements in a layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.image)
        self.setLayout(layout)
        # Prepare the panel
        self.panel = GraphPanel(self, parent=self.image)
        self.panel.hidden.connect(self.toolbar.toggle_edit_action)
        # Connect to the controller
        self.ctl.executed.connect(self._function_executed)
        self.ctl.execute_error.connect(self._function_execute_error)
        self.ctl.finished.connect(self._function_finished)
        self.ctl.deleted.connect(self._function_deleted)
        self.ctl.finished.connect(self.toolbar.function_finished)
        self.ctl.created.connect(self.toolbar.function_saved)
        self.ctl.updated.connect(self.toolbar.function_saved)
        self.ctl.deleted.connect(self.toolbar.function_deleted)

    def set_form(self, form):
        """Integrate form inside the panel."""
        self.panel.setLayout(form)
        form.data_changed.connect(self._function_unsaved)
        form.data_changed.connect(self.toolbar.function_unsaved)
        form.data_restored.connect(self._function_restored)
        form.data_restored.connect(self.toolbar.function_restored)

    def show_panel(self, show=True):
        """Show the panel."""
        if show:
            self.panel.show()
        else:
            self.panel.hide()

    def export(self):
        """Export the graph (image) in a format among (some of) those
        supported by Graphviz.
        """
        formats = [
            # images
            (u"%s (*.bmp)" % _(u"Image Windows BMP"), [u'.bmp']),
            (u"%s (*.jpg *.jpeg *.jpe)" % _(u"Image JPEG"), [
                u'.jpg', u'.jpeg', u'jpe']),
            (u"%s (*.gif)" % _(u"Image GIF"), [u'.gif']),
            (u"%s (*.png)" % _(u"Image PNG"), [u'.png']),
            # other
            (u"%s (*.dot)" % (u"DOT"), [u'.dot']),
            (u"%s (*.pdf)" % (u"PDF"), [u'.pdf']),
            (u"%s (*.ps)" % (u"PostScript"), [u'.ps']),
            (u"%s (*.eps)" % (u"Encapsulated PostScript"), [u'.eps']),
            (u"%s (*.svg)" % (u"SVG"), [u'.svg']),
            (u"%s (*.svgz)" % (u"SVGz"), [u'.svgz']),
        ]
        default_format = u"%s (*.png)" % _(u"Image PNG")
        if self.graph:
            data = self.panel.get_data()
            name = data.get('name', u"%s" % self._model).replace('.', '_')
            path, format_ = QtGui.QFileDialog.getSaveFileName(
                self, _(u"Export"), name,
                u';;'.join([fmt[0] for fmt in formats]), default_format)
            if path:
                # Detect the extension from the file name without taking into
                # account the selected extension in the list
                path_ext = None
                for fmt in formats:
                    exts = fmt[1]
                    for ext in exts:
                        if path.endswith(ext):
                            path_ext = ext
                            break
                    if path_ext:
                        break
                # If no extension was typed in the file name, we take the
                # selected one in the list
                if not path_ext:
                    for fmt in formats:
                        if fmt[0] == format_:
                            path_ext = fmt[1][0]
                            path += path_ext
                            break
                # Save the graph (pydot/Graphviz manages that for us)
                self.graph.write(path, format=path_ext[1:])

    def save(self):
        """Save the user parameters."""
        data = self.panel.get_data()
        if self.new:
            id_tmp = self.id_
            self.id_ = self.ctl.create(data)
            self.created.emit(self._model, id_tmp, self.id_)
            self.new = False
        else:
            self.ctl.update(self.id_, data)
        self.unsaved = False

    def restore(self):
        """Restore original data."""
        if not self.new:
            data = self.ctl.read(self.id_)
            self.panel.layout().set_data(data)

    def execute(self):
        """Execute the function."""
        data = self.panel.get_data()
        self.ctl.execute(self.id_, data)

    def _function_unsaved(self):
        """Set the workarea as 'Unsaved' when data are changed."""
        self.unsaved = True
        self.data_changed.emit(self._model, self.id_, self.panel.get_data())

    def _function_restored(self):
        """Notify listeners that the data has been restored.."""
        self.unsaved = False
        self.data_restored.emit(self._model, self.id_, self.panel.get_data())

    def _function_executed(self, model, id_):
        """Update the workarea when the function is executed."""
        if self.id_ == id_:
            self.toolbar.setEnabled(False)
            self.image.setEnabled(False)

    def _function_execute_error(self, model, id_):
        """Set the workarea in a good state if an error occurred."""
        if self.id_ == id_:
            self.toolbar.setEnabled(True)
            self.image.setEnabled(True)

    def _function_finished(self, model, id_, graph):
        """Update the workarea with `data` when the function is finished."""
        if self.id_ == id_:
            self.graph = graph
            img_png = self.graph.make_dot().create_png()
            self.image.update_image(img_png)
            if self.image.is_large():
                self.image.zoom_fit_best()
            self.toolbar.setEnabled(True)
            self.image.setEnabled(True)

    def _function_deleted(self, model, id_):
        """Set the workarea as 'New' when the function is deleted."""
        if self.id_ == id_:
            self.new = True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

