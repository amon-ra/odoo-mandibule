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
from PySide.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, header, default, data=None, *args):
        """`data` is a two dimensional table and `header` defines header keys:

            >>> data = [['sale.order', True, False, True], ...]
            >>> header = ["Model", "Base", "Show", "Attr."]
            >>> model = TableModel(self, data, header)
            >>> view = QTableView()
            >>> view.setModel(model)
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self._data = data or []
        self._header = header
        self._default = default
        if len(self._default) != len(self._header):
            raise ValueError(
                u"Number of default values is different than the "
                u"number of columns.")

    def insert_data(self, data):
        self._data = data
        self.reset()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._header)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        value = self._data[index.row()][index.column()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return value
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False
        if index.isValid() and 0 <= index.row() < len(self._data):
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal \
                and role == QtCore.Qt.DisplayRole:
            return self._header[section]
        return None

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        for x in range(count):
            self._data.insert(row + x, self._default[:])
        self.endInsertRows()
        index = QtCore.QModelIndex()
        self.dataChanged.emit(index, index)
        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        #self.beginRemoveRows(QtCore.QtCore.QModelIndex(), row, row + count - 1)
        del self._data[row:(row + count)]
        self.endRemoveRows()
        index = QtCore.QModelIndex()
        self.dataChanged.emit(index, index)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
