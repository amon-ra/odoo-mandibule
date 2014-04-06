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
from PySide import QtGui, QtCore


class Common(QtCore.QObject):
    changed = QtCore.Signal()


class SelectField(Common):
    def __init__(self, label, choices, default=None, **kwargs):
        """
        param choice tuple(label, value)
        param default value
        """
        Common.__init__(self)
        self.label = label
        self.widget = QtGui.QComboBox()
        self.widget.currentIndexChanged.connect(
            lambda *args: self.changed.emit())
        values = []
        for name, value in choices:
            self.widget.addItem(name, userData=value)
            values.append(value)

        if default and default in values:
            index = values.index(default)
            self.widget.setCurrentIndex(index)

    def set_value(self, value):
        index = self.widget.findData(value)
        self.widget.setCurrentIndex(index)

    @property
    def result(self):
        index = self.widget.currentIndex()
        return (self.widget.itemText(index), self.widget.itemData(index))


class TextField(Common):
    def __init__(self, label, default="", multi=False, **kwargs):
        Common.__init__(self)
        self.label = label
        self._multi = multi
        if self._multi:
            self.widget = QtGui.QTextEdit()
        else:
            self.widget = QtGui.QLineEdit()
        self.widget.textChanged.connect(
            lambda *args: self.changed.emit())
        self.widget.setText(default)

    def set_value(self, value):
        self.widget.setText(value)

    @property
    def result(self):
        if self._multi:
            return self.widget.toPlainText()
        return self.widget.text()


class PasswordField(TextField):
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(*args, **kwargs)
        self.widget.setEchoMode(QtGui.QLineEdit.Password)


class IntField(Common):
    def __init__(self, label, default=0, range_=(0, 100), **kwargs):
        Common.__init__(self)
        self.label = label
        self.widget = QtGui.QSpinBox()
        self.widget.valueChanged.connect(
            lambda *args: self.changed.emit())
        self.widget.setRange(*(range_))
        self.widget.setValue(default)

    def set_value(self, value):
        self.widget.setValue(value)

    @property
    def result(self):
        return self.widget.value()


class BoolField(Common):
    def __init__(self, label, default=False, **kwargs):
        Common.__init__(self)
        self.label = label
        self.widget = QtGui.QCheckBox()
        self.widget.stateChanged.connect(
            lambda *args: self.changed.emit())
        self.widget.setTristate(False)
        self.widget.setChecked(default)

    def set_value(self, value):
        self.widget.setChecked(value)

    @property
    def result(self):
        return self.widget.isChecked()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
