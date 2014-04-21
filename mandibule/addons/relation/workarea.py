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
"""Workarea widgets."""
from PySide import QtCore, QtGui

from mandibule.reg import WorkArea, Controller, Icons
from mandibule.utils.i18n import _
from mandibule.widgets.graph import GraphFormLayout, GraphWorkArea
from mandibule.widgets.fields import TextField, IntField, BoolField
from mandibule.widgets.delegate import CheckBoxDelegate
from mandibule.widgets.model import TableModel


class RelationTableModel(TableModel):
    """Data model used by the table view on the form to manage
    OpenERP models displayed on graph.
    """

    def flags(self, index):
        """Overloaded to disable some columns following input values."""
        flags = super(RelationTableModel, self).flags(index)
        name = self._data[index.row()][0]
        root_ok = self._data[index.row()][1]
        show_ok = self._data[index.row()][2]
        if index.column() == 1 and name and '*' in name :
            flags &= ~ QtCore.Qt.ItemIsEnabled
        if index.column() == 2 and root_ok:
            flags &= ~ QtCore.Qt.ItemIsEnabled
        if index.column() == 3 and not show_ok:
            flags &= ~ QtCore.Qt.ItemIsEnabled
        return flags

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Overloaded to dynamically update other columns accordingly."""
        if index.column() == 0:
            value = value.strip().lower()
            if ' ' in value:
                raise ValueError(
                    _(u"Space characters are not allowed."))
        res = super(RelationTableModel, self).setData(index, value, role)
        if res:
            index_root_ok = self.index(index.row(), 1)
            index_show_ok = self.index(index.row(), 2)
            index_attr_ok = self.index(index.row(), 3)
            # 'name' contains the joker character => 'root_ok' = False
            if index.column() == 0 and '*' in value:
                self.setData(index_root_ok, False)
                self.dataChanged.emit(index_root_ok, index_root_ok)
            # 'root_ok' == True => 'show_ok' = True
            if index.column() == 1:
                if value:
                    self.setData(index_show_ok, True)
                self.dataChanged.emit(index_show_ok, index_show_ok)
            # 'show_ok' updated => update 'attr_ok'
            if index.column() == 2:
                self.dataChanged.emit(index_attr_ok, index_attr_ok)
        return res


class RelationFormLayout(GraphFormLayout):
    """Describe the form for a models relations graph."""

    def __init__(self, workarea, id_=None):
        # Table view
        self.table = QtGui.QTableView()
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setItemDelegateForColumn(1, CheckBoxDelegate(self.table))
        self.table.setItemDelegateForColumn(2, CheckBoxDelegate(self.table))
        self.table.setItemDelegateForColumn(3, CheckBoxDelegate(self.table))
        #self.table.setSizePolicy(
        #    QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.table.verticalHeader().hide()
        #self.table.setSortingEnabled(True)
        #self.table.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.table.setMinimumHeight(300)
        # Table data model
        table_model = RelationTableModel(
            self.table,
            header=[_(u"Model"), _(u"Base"), _(u"Show"), _(u"Attr.")],
            default=[u"", False, True, True])
        self.table.setModel(table_model)
        # Buttons to add add/remove rows
        self.button_add = QtGui.QPushButton(
            Icons['add'], _(u"Add"))
        self.button_add.clicked.connect(self._button_add_clicked)
        self.button_rm = QtGui.QPushButton(
            Icons['remove'], _(u"Remove"))
        self.button_rm.clicked.connect(self._button_rm_clicked)
        self.button_rm.setEnabled(False)
        # Super first
        super(RelationFormLayout, self).__init__(workarea, id_)
        # Then connect to signals
        table_model.dataChanged.connect(lambda item: self.data_changed.emit())
        table_model.dataChanged.connect(self._function_unsaved)
        table_model.modelReset.connect(self._update_buttons)
        selection_model = self.table.selectionModel()
        selection_model.selectionChanged.connect(self._update_buttons)

    def init_fields(self, data):
        """Prepare and insert fields in the form."""
        self.fields['name'] = TextField(_("Name"), data.get('name', ''))
        self.addRow(
            self.fields['name'].label, self.fields['name'].widget)
        self.fields['maxdepth'] = IntField(
            _(u"Level"), data.get('maxdepth', 1), range_=(0, 42))
        self.fields['autocompletion'] = BoolField(
            _("Autocompletion"), data.get('autocompletion', True))
        # Insert the table view with its buttons
        table_buttons = QtGui.QHBoxLayout()
        table_buttons.setContentsMargins(0, 0, 0, 0)
        table_buttons.addWidget(self.button_add)
        table_buttons.addWidget(self.button_rm)
        label = QtGui.QLabel(self.fields['maxdepth'].label)
        label.setAlignment(QtCore.Qt.AlignCenter)
        table_buttons.addWidget(label)
        table_buttons.addWidget(self.fields['maxdepth'].widget)
        label = QtGui.QLabel(self.fields['autocompletion'].label)
        label.setAlignment(QtCore.Qt.AlignCenter)
        table_buttons.addWidget(label)
        table_buttons.addWidget(self.fields['autocompletion'].widget)
        self.addRow(table_buttons)
        self.addRow(self.table)
        # Insert data in fields and tables
        self.set_data(data)

    def get_data(self):
        """Return user input data."""
        # Get data from the table
        data = {
            'server_id': self.workarea.server_id,
            'name': self.fields['name'].result,
            'maxdepth': self.fields['maxdepth'].result,
            'autocompletion': self.fields['autocompletion'].result,
            'models': [],
            'whitelist': [],
            'blacklist': [],
            'attrs_whitelist': [],
            'attrs_blacklist': [],
        }
        for row in range(self.table.model().rowCount()):
            model = self.table.model()
            name = model.index(row, 0).data(QtCore.Qt.DisplayRole)
            root_ok = model.index(row, 1).data(QtCore.Qt.DisplayRole)
            show_ok = model.index(row, 2).data(QtCore.Qt.DisplayRole)
            attr_ok = model.index(row, 3).data(QtCore.Qt.DisplayRole)
            if root_ok and name not in data['models']:
                data['models'].append(name)
            if show_ok and name not in data['whitelist']:
                data['whitelist'].append(name)
            if not show_ok and name not in data['blacklist']:
                data['blacklist'].append(name)
            if attr_ok and name not in data['attrs_whitelist']:
                data['attrs_whitelist'].append(name)
            if not attr_ok and name not in data['attrs_blacklist']:
                data['attrs_blacklist'].append(name)
        # FIXME: use lists later, need to update controllers and migrate
        # the user configuration file
        for field in ['models', 'whitelist', 'blacklist',
                      'attrs_whitelist', 'attrs_blacklist']:
            data[field] = ' '.join(data[field])
        return data

    def set_data(self, data):
        """Inject `data` in the form."""
        self.blockSignals(True)
        self.table.blockSignals(True)

        self.fields['name'].set_value(data.get('name', u""))
        self.fields['maxdepth'].set_value(data.get('maxdepth', 1))
        self.fields['autocompletion'].set_value(
            data.get('autocompletion', False))
        # Prepare data for the table
        table_data = {}
        line = {'root_ok': False, 'show_ok': True, 'attr_ok': True}
        for model in data['models'].split():
            if model not in table_data:
                table_data[model] = line.copy()
                table_data[model]['root_ok'] = True
        for model in data['whitelist'].split():
            if model not in table_data:
                table_data[model] = line.copy()
            table_data[model]['show_ok'] = True
        for model in data['blacklist'].split():
            if model not in table_data:
                table_data[model] = line.copy()
            table_data[model]['show_ok'] = False
        for model in data['attrs_whitelist'].split():
            if model not in table_data:
                table_data[model] = line.copy()
            table_data[model]['attr_ok'] = True
        for model in data['attrs_blacklist'].split():
            if model not in table_data:
                table_data[model] = line.copy()
            table_data[model]['attr_ok'] = False
        rows = [[model] + [vals['root_ok'], vals['show_ok'], vals['attr_ok']]
                for model, vals in table_data.iteritems()]
        # Insert data in the table model
        self.table.model().insert_data(rows)
        self.table.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.blockSignals(False)
        self.table.blockSignals(False)
        self.data_restored.emit()

    def _update_buttons(self):
        """Called when the selection changed to update the state of the
        remove button.
        """
        if self.table.selectionModel().selection().empty():
            self.button_rm.setEnabled(False)
        else:
            self.button_rm.setEnabled(True)

    def _button_add_clicked(self):
        """Insert a new row in the table and give the focus to it."""
        self.table.model().insertRows(0, 1)
        self.table.selectRow(0)
        index = self.table.selectedIndexes()[0]
        self.table.edit(index)

    def _button_rm_clicked(self):
        """Remove selected rows in the table."""
        rows = [row.row()
                for row in self.table.selectionModel().selectedRows()]
        # To avoid index offset while removing rows, delete last rows first
        rows.reverse()
        for row in rows:
            self.table.model().removeRows(row, 1)


class RelationWorkArea(GraphWorkArea):
    """Relations graph workarea."""
    __metadata__ = {
        'name': 'relation',
    }

    def __init__(self, app, server_id, id_=None, new=False):
        GraphWorkArea.__init__(self, app, 'relation', server_id, id_, new)
        form = RelationFormLayout(self, id_)
        self.set_form(form)

    def _function_finished(self, model, id_, data, graph):
        """Overloaded to autocomplete the list of models."""
        super(RelationWorkArea, self)._function_finished(
            model, id_, data, graph)
        if self.id_ == id_:
            if data.get('autocompletion'):
                changed = False
                for model in graph._relations:
                    if model not in data['whitelist'] \
                            and model not in data['blacklist']:
                        data['whitelist'] += u' ' + model
                        changed = True
                if changed:
                    self.panel.layout().set_data(data)
                    self.panel.layout().table.model().dataChanged.emit(0, 0)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
