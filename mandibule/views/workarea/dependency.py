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
from mandibule.views.widgets.fields import TextField, BoolField
from mandibule.views.workarea.content import GraphFormLayout, GraphContent
from mandibule.views.widgets.delegate import CheckBoxDelegate
from mandibule.views.widgets.model import TableModel


class DependencyModuleTableModel(TableModel):
    """Data model used by the table view on the form to manage
    OpenERP starting/root modules to display on graph.
    """

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Overloaded to dynamically update other columns accordingly."""
        if index.column() == 0:
            value = value.strip().lower()
            if ' ' in value:
                raise ValueError(
                    _(u"Space characters are not allowed."))
        return super(DependencyModuleTableModel, self).setData(
            index, value, role)


class DependencyModelTableModel(TableModel):
    """Data model used by the table view on the form to manage
    OpenERP data models to display on graph.
    """

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Overloaded to dynamically update other columns accordingly."""
        if index.column() == 0:
            value = value.strip().lower()
            if ' ' in value:
                raise ValueError(
                    _(u"Space characters are not allowed."))
        return super(DependencyModelTableModel, self).setData(
            index, value, role)


class DependencyFormLayout(GraphFormLayout):
    """Describe the form for a modules dependencies graph."""

    def __init__(self, content, id_=None):
        # Modules table view
        self.table_modules = QtGui.QTableView()
        self.table_modules.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.table_modules.verticalHeader().hide()
        self.table_modules.setMinimumHeight(90)
        self.table_modules.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.ResizeToContents)
        self.table_modules.horizontalHeader().setResizeMode(
            0, QtGui.QHeaderView.Stretch)
        # Modules table data model
        table_modules_model = DependencyModuleTableModel(
            self.table_modules,
            header=[_(u"Root module")],
            default=[u""])
        self.table_modules.setModel(table_modules_model)
        # Buttons to add add/remove modules
        self.button_module_add = QtGui.QPushButton(
            content.app.icons.icon_add, _(u"Add"))
        self.button_module_add.clicked.connect(self._button_module_add_clicked)
        self.button_module_rm = QtGui.QPushButton(
            content.app.icons.icon_remove, _(u"Remove"))
        self.button_module_rm.clicked.connect(self._button_module_rm_clicked)
        self.button_module_rm.setEnabled(False)
        # Models table view
        self.table_models = QtGui.QTableView()
        self.table_models.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.table_models.setItemDelegateForColumn(
            1, CheckBoxDelegate(self.table_models))
        self.table_models.verticalHeader().hide()
        self.table_models.setMinimumHeight(200)
        self.table_models.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.ResizeToContents)
        self.table_models.horizontalHeader().setResizeMode(
            0, QtGui.QHeaderView.Stretch)
        # Models table data model
        table_models_model = DependencyModelTableModel(
            self.table_models,
            header=[_(u"Model"), _(u"Show")],
            default=[u"", True])
        self.table_models.setModel(table_models_model)
        # Buttons to add add/remove models
        self.button_model_add = QtGui.QPushButton(
            content.app.icons.icon_add, _(u"Add"))
        self.button_model_add.clicked.connect(self._button_model_add_clicked)
        self.button_model_rm = QtGui.QPushButton(
            content.app.icons.icon_remove, _(u"Remove"))
        self.button_model_rm.clicked.connect(self._button_model_rm_clicked)
        self.button_model_rm.setEnabled(False)
        # Super first
        super(DependencyFormLayout, self).__init__(content, id_)
        # Then connect to signals
        table_modules_model.dataChanged.connect(
            lambda item: self.data_changed.emit())
        table_modules_model.dataChanged.connect(self.function_unsaved)
        table_modules_model.modelReset.connect(self._update_buttons)
        self.table_modules.selectionModel().selectionChanged.connect(
            self._update_buttons)
        table_models_model.dataChanged.connect(
            lambda item: self.data_changed.emit())
        table_models_model.dataChanged.connect(self.function_unsaved)
        table_models_model.modelReset.connect(self._update_buttons)
        self.table_models.selectionModel().selectionChanged.connect(
            self._update_buttons)

    def init_fields(self, data):
        """Prepare and insert fields in the form."""
        self.fields['name'] = TextField(_("Name"), data.get('name', ''))
        self.addRow(
            self.fields['name'].label,
            self.fields['name'].widget)
        # Insert the modules table view with its buttons
        table_buttons = QtGui.QHBoxLayout()
        table_buttons.setContentsMargins(0, 0, 0, 0)
        table_buttons.addWidget(self.button_module_add)
        table_buttons.addWidget(self.button_module_rm)
        self.addRow(table_buttons)
        self.addRow(self.table_modules)
        # Insert a separator
        separator = QtGui.QFrame()
        #separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameStyle(QtGui.QFrame.HLine | QtGui.QFrame.Sunken)
        self.addRow(separator)
        # Insert the models table view with its buttons
        table_buttons = QtGui.QHBoxLayout()
        table_buttons.setContentsMargins(0, 0, 0, 0)
        table_buttons.addWidget(self.button_model_add)
        table_buttons.addWidget(self.button_model_rm)
        self.addRow(table_buttons)
        self.addRow(self.table_models)
        # Restrict models checkbox
        self.fields['restrict'] = BoolField(
            _("Restrict to models"), data.get('restrict', False))
        self.addRow(
            self.fields['restrict'].label,
            self.fields['restrict'].widget)

        # Insert data in fields and tables
        self.set_data(data)

    def get_data(self):
        """Return user input data."""
        # Get data from the tables
        data = {
            'server_id': self.content.server_id,
            'name': self.fields['name'].result,
            'modules': [],
            'models': [],
            'models_blacklist': [],
            'restrict': self.fields['restrict'].result,
        }
        # Modules
        for row in range(self.table_modules.model().rowCount()):
            model = self.table_modules.model()
            name = model.index(row, 0).data(QtCore.Qt.DisplayRole)
            if name not in data['modules']:
                data['modules'].append(name)
        # Models
        for row in range(self.table_models.model().rowCount()):
            model = self.table_models.model()
            name = model.index(row, 0).data(QtCore.Qt.DisplayRole)
            show_ok = model.index(row, 1).data(QtCore.Qt.DisplayRole)
            if show_ok and name not in data['models']:
                data['models'].append(name)
            if not show_ok and name not in data['models_blacklist']:
                data['models_blacklist'].append(name)
        # FIXME: use lists later, need to update controllers and migrate
        # the user configuration file
        for field in ['modules', 'models', 'models_blacklist']:
            data[field] = ' '.join(data[field])
        return data

    def set_data(self, data):
        """Inject `data` in the form."""
        self.blockSignals(True)
        self.table_modules.blockSignals(True)

        self.fields['name'].set_value(data.get('name', u""))
        self.fields['restrict'].set_value(data.get('restrict', False))
        # Insert data in the modules table model
        rows = [[module] for module in data['modules'].split()]
        self.table_modules.model().insert_data(rows)
        self.table_modules.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.ResizeToContents)
        self.table_modules.horizontalHeader().setResizeMode(
            0, QtGui.QHeaderView.Stretch)
        # Prepare data for the models table model
        table_data = {}
        line = {'show_ok': True}
        for model in data['models'].split():
            if model not in table_data:
                table_data[model] = line.copy()
                table_data[model]['show_ok'] = True
        for model in data['models_blacklist'].split():
            if model not in table_data:
                table_data[model] = line.copy()
            table_data[model]['show_ok'] = False
        rows = [[model] + [vals['show_ok']]
                for model, vals in table_data.iteritems()]
        # Insert data in the models table model
        self.table_models.model().insert_data(rows)
        self.table_models.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.ResizeToContents)
        self.table_models.horizontalHeader().setResizeMode(
            0, QtGui.QHeaderView.Stretch)

        self.blockSignals(False)
        self.table_modules.blockSignals(False)
        self.data_restored.emit()

    def _update_buttons(self):
        """Called when the selection changed on the modules or models tables
        to update the state of the remove button.
        """
        # Modules buttons
        if self.table_modules.selectionModel().selection().empty():
            self.button_module_rm.setEnabled(False)
        else:
            self.button_module_rm.setEnabled(True)
        # Models buttons
        if self.table_models.selectionModel().selection().empty():
            self.button_model_rm.setEnabled(False)
        else:
            self.button_model_rm.setEnabled(True)

    def _button_module_add_clicked(self):
        """Insert a new row in the modules table and give the focus to it."""
        self.table_modules.model().insertRows(0, 1)
        self.table_modules.selectRow(0)
        index = self.table_modules.selectedIndexes()[0]
        self.table_modules.edit(index)

    def _button_module_rm_clicked(self):
        """Remove selected rows in the modules table."""
        rows = [row.row()
                for row in self.table_modules.selectionModel().selectedRows()]
        # To avoid index offset while removing rows, delete last rows first
        rows.reverse()
        for row in rows:
            self.table_modules.model().removeRows(row, 1)

    def _button_model_add_clicked(self):
        """Insert a new row in the models table and give the focus to it."""
        self.table_models.model().insertRows(0, 1)
        self.table_models.selectRow(0)
        index = self.table_models.selectedIndexes()[0]
        self.table_models.edit(index)

    def _button_model_rm_clicked(self):
        """Remove selected rows in the models table."""
        rows = [row.row()
                for row in self.table_models.selectionModel().selectedRows()]
        # To avoid index offset while removing rows, delete last rows first
        rows.reverse()
        for row in rows:
            self.table_models.model().removeRows(row, 1)


class DependencyContent(GraphContent):
    """Dependencies graph content."""

    def __init__(self, app, server_id, id_=None, new=False):
        ctl = app.dependency_ctl
        GraphContent.__init__(self, app, ctl, server_id, id_, new)
        form = DependencyFormLayout(self, id_)
        self.set_form(form)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
