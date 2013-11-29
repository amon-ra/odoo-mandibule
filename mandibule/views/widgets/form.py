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
from PySide import QtGui


class SelectField(object):
    def __init__(self, label, choices, default=None, **kwargs):
        """
        param choice tuple(label, value)
        param default value
        """
        self.label = label
        self.widget = QtGui.QComboBox()
        values = []
        for name, value in choices:
            self.widget.addItem(name, userData=value)
            values.append(value)

        if default and default in values:
            index = values.index(default)
            self.widget.setCurrentIndex(index)

    @property
    def result(self):
        index = self.widget.currentIndex()
        return (self.widget.itemText(index), self.widget.itemData(index))


class TextField(object):
    def __init__(self, label, default="", multi=False, **kwargs):
        self.label = label
        self._multi = multi
        if self._multi:
            self.widget = QtGui.QTextEdit()
        else:
            self.widget = QtGui.QLineEdit()
        self.widget.setText(default)

    @property
    def result(self):
        if self._multi:
            return self.widget.toPlainText()
        return self.widget.text()


class PasswordField(TextField):
    def __init__(self, label, **kwargs):
        super(PasswordField, self).__init__(label)
        self.widget.setEchoMode(QtGui.QLineEdit.Password)


class IntField(object):
    def __init__(self, label, default=0, range_=(0, 100), **kwargs):
        self.label = label
        self.widget = QtGui.QSpinBox()
        self.widget.setRange(*(range_))
        self.widget.setValue(default)

    @property
    def result(self):
        return self.widget.value()


class BoolField(object):
    def __init__(self, label, default=False, **kwargs):
        self.label = label
        self.widget = QtGui.QCheckBox()
        self.widget.setTristate(False)
        self.widget.setChecked(default)

    @property
    def result(self):
        return self.widget.isChecked()


class FormDialog(object):
    def __init__(self, schema):
        self._result = {}
        self._schema = schema
        self._items = {}
        self.dial = QtGui.QDialog()
        layout = self.get_layout()
        buttons = QtGui.QDialogButtonBox(
                QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel,
                parent=self.dial
                )

        layout.addWidget(buttons)
        buttons.accepted.connect(self.ok)
        buttons.rejected.connect(self.reject)


        self.dial.setLayout(layout)
        self._first.setFocus()

    def get_layout(self):
        layout = QtGui.QFormLayout()
        self._first = None
        for name, field in self._schema:
            layout.addRow(field.label, field.widget)
            if not self._first:
                self._first = field.widget
        return layout

    def reject(self):
        self.dial.reject()

    def exec_(self):
        if self.dial.exec_():
            return self._result, True
        return None, False


    def ok(self):
        for name, field in self._schema:
            self._result[name] = field.result
        self.dial.accept()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
