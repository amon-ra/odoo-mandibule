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


class GraphPanel(QtGui.QScrollArea):
    """Panel used inside a `GraphContent`."""
    hidden = QtCore.Signal(bool)

    def __init__(self, content, parent=None, layout=None):
        QtGui.QScrollArea.__init__(self, parent)
        self.content = content
        self.setFrameStyle(QtGui.QFrame.WinPanel | QtGui.QFrame.Plain)
        if layout:
            self.setLayout(layout)
        self.hide()

    def setLayout(self, layout):
        """Set the content of the panel."""
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

    def __init__(self, content, id_=None):
        QtGui.QFormLayout.__init__(self)
        self.content = content
        ctl = self.content.ctl
        icons = self.content.app.icons
        data = id_ and ctl.read(id_) \
            or ctl.default_get({'server_id': content.server_id})
        # Fields
        self.fields = {}
        self.init_fields(data)
        # Buttons
        self.button_save = QtGui.QPushButton(icons.icon_save, _(u"Save"))
        self.button_save.clicked.connect(self.content.save)
        self.button_save.setEnabled(self.content.unsaved)
        self.button_restore = QtGui.QPushButton(icons.icon_undo, _(u"Undo"))
        self.button_restore.clicked.connect(self.content.restore)
        self.button_restore.setEnabled(False)
        self.button_close = QtGui.QPushButton(icons.icon_ok, _(u"Close"))
        self.button_close.clicked.connect(
            lambda: self.content.show_panel(False))
        self.button_execute = QtGui.QPushButton(icons.icon_exe, _(u"Execute"))
        self.button_execute.clicked.connect(self.content.execute)
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
            field.changed.connect(self.function_unsaved)
        ctl.created.connect(self.function_saved)
        ctl.updated.connect(self.function_saved)
        ctl.deleted.connect(self.function_unsaved)
        self.data_restored.connect(self.function_restored)

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

    def function_saved(self, *args):
        """Disable the save button once the function is saved."""
        self.button_save.setEnabled(False)
        self.button_restore.setEnabled(False)

    def function_unsaved(self, *args):
        """Enable the save button once the function is deleted."""
        self.button_save.setEnabled(True)
        if not self.content.new:
            self.button_restore.setEnabled(True)

    def function_restored(self, *args):
        """Disable the save button once the function is restored."""
        self.button_save.setEnabled(False)
        self.button_restore.setEnabled(False)


class GraphContentToolbar(QtGui.QToolBar):
    """Toolbar used inside a `GraphContent`."""

    def __init__(self, content):
        QtGui.QToolBar.__init__(self)
        self.content = content
        icons = self.content.app.icons
        self.setIconSize(QtCore.QSize(16, 16))
        self._actions = {}
        # Save
        self._actions['save'] = QtGui.QAction(
            icons.icon_save, _(u"Save function"), self)
        self._actions['save'].setShortcut('Ctrl+S')
        self._actions['save'].setEnabled(False)
        self._actions['save'].triggered.connect(self.content.save)
        self.addAction(self._actions['save'])
        # Restore modifications
        self._actions['restore'] = QtGui.QAction(
            icons.icon_undo, _(u"Undo modifications"), self)
        self._actions['restore'].setShortcut('Ctrl+U')
        self._actions['restore'].setEnabled(False)
        self._actions['restore'].triggered.connect(self.content.restore)
        self.addAction(self._actions['restore'])
        # Edit parameters
        self._actions['edit'] = QtGui.QAction(
            icons.icon_edit, _(u"Edit parameters"), self)
        self._actions['edit'].setShortcut('Ctrl+E')
        self._actions['edit'].setCheckable(True)
        self._actions['edit'].toggled.connect(self.content.show_panel)
        self.addAction(self._actions['edit'])
        self.addSeparator()
        # Execute
        self._actions['execute'] = QtGui.QAction(
            icons.icon_exe, _(u"Execute"), self)
        self._actions['execute'].setShortcut('Ctrl+X')
        self._actions['execute'].triggered.connect(self.content.execute)
        self.addAction(self._actions['execute'])
        self.addSeparator()
        # Zoom in
        self._actions['zoom_in'] = QtGui.QAction(
            icons.icon_zoom_in, _(u"Zoom in"), self)
        self._actions['zoom_in'].setShortcut('Ctrl++')
        self._actions['zoom_in'].setEnabled(False)
        self._actions['zoom_in'].triggered.connect(
            self.content.image.zoom_in)
        self.addAction(self._actions['zoom_in'])
        # Zoom out
        self._actions['zoom_out'] = QtGui.QAction(
            icons.icon_zoom_out, _(u"Zoom out"), self)
        self._actions['zoom_out'].setShortcut('Ctrl+-')
        self._actions['zoom_out'].setEnabled(False)
        self._actions['zoom_out'].triggered.connect(
            self.content.image.zoom_out)
        self.addAction(self._actions['zoom_out'])
        # Zoom original
        self._actions['zoom_orig'] = QtGui.QAction(
            icons.icon_zoom_orig, _(u"Original size"), self)
        self._actions['zoom_orig'].setShortcut('Ctrl+0')
        self._actions['zoom_orig'].setEnabled(False)
        self._actions['zoom_orig'].triggered.connect(
            self.content.image.zoom_original)
        self.addAction(self._actions['zoom_orig'])
        # Zoom fit best
        self._actions['zoom_fit_best'] = QtGui.QAction(
            icons.icon_zoom_fit, _(u"Fit to window"), self)
        self._actions['zoom_fit_best'].setShortcut('Ctrl+=')
        self._actions['zoom_fit_best'].setEnabled(False)
        self._actions['zoom_fit_best'].triggered.connect(
            self.content.image.zoom_fit_best)
        self.addAction(self._actions['zoom_fit_best'])

    def toggle_edit_action(self, not_toggled):
        self._actions['edit'].setChecked(not not_toggled)

    def function_saved(self, *args):
        self._actions['save'].setEnabled(False)
        self._actions['restore'].setEnabled(False)

    def function_unsaved(self):
        self._actions['save'].setEnabled(True)
        if not self.content.new:
            self._actions['restore'].setEnabled(True)

    def function_restored(self, *args):
        self._actions['save'].setEnabled(False)
        self._actions['restore'].setEnabled(False)

    def function_deleted(self, *args):
        self._actions['save'].setEnabled(True)

    def function_finished(self):
        for action in ['zoom_in', 'zoom_out', 'zoom_orig', 'zoom_fit_best']:
            self._actions[action].setEnabled(True)


class GraphContent(QtGui.QWidget):
    """Abstract content widget to represent and manage a graph."""
    data_changed = QtCore.Signal(str, dict)
    data_restored = QtCore.Signal(str, dict)

    def __init__(self, app, ctl, server_id, id_=None, new=False):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.ctl = ctl
        self.server_id = server_id
        self.id_ = id_
        self.new = new
        self.unsaved = False
        # Image and toolbar
        self.image = ZoomableImage()
        self.toolbar = GraphContentToolbar(self)
        # Place elements in a layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.image)
        self.setLayout(layout)
        # Prepare the panel
        self.panel = GraphPanel(self, parent=self.image)
        self.panel.hidden.connect(self.toolbar.toggle_edit_action)
        # Connect to the controller
        self.ctl.executed.connect(self.function_executed)
        self.ctl.execute_error.connect(self.function_execute_error)
        self.ctl.finished.connect(self.function_finished)
        self.ctl.deleted.connect(self.function_deleted)
        self.ctl.finished.connect(self.toolbar.function_finished)
        self.ctl.created.connect(self.toolbar.function_saved)
        self.ctl.updated.connect(self.toolbar.function_saved)
        self.ctl.deleted.connect(self.toolbar.function_deleted)

    def set_form(self, form):
        """Integrate form inside the panel."""
        self.panel.setLayout(form)
        form.data_changed.connect(self.function_unsaved)
        form.data_changed.connect(self.toolbar.function_unsaved)
        form.data_restored.connect(self.function_restored)
        form.data_restored.connect(self.toolbar.function_restored)

    def show_panel(self, show=True):
        """Show the panel."""
        if show:
            self.panel.show()
        else:
            self.panel.hide()

    def save(self):
        """Save the user parameters."""
        data = self.panel.get_data()
        if self.new:
            self.id_ = self.ctl.create(data, {'from_id_tmp': self.id_})
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

    def function_unsaved(self):
        """Set the content as 'Unsaved' when data are changed."""
        self.unsaved = True
        self.data_changed.emit(self.id_, self.panel.get_data())

    def function_restored(self):
        """Notify listeners that the data has been restored.."""
        self.unsaved = False
        self.data_restored.emit(self.id_, self.panel.get_data())

    def function_executed(self, id_, context):
        """Update the content when the function is executed."""
        if id_ == self.id_:
            self.toolbar.setEnabled(False)
            self.image.setEnabled(False)

    def function_execute_error(self, id_):
        """Set the content in a good state if an error occurred."""
        if id_ == self.id_:
            self.toolbar.setEnabled(True)
            self.image.setEnabled(True)

    def function_finished(self, id_, data):
        """Update the content with `data` when the function is finished."""
        if id_ == self.id_:
            self.image.update_image(data[0])
            if self.image.is_large():
                self.image.zoom_fit_best()
            self.toolbar.setEnabled(True)
            self.image.setEnabled(True)

    def function_deleted(self, id_, context):
        """Set the content as 'New' when the function is deleted."""
        if id_ == self.id_:
            self.new = True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
