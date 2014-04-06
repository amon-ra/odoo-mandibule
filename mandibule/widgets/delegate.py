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


class CheckBoxDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        """Paint a checkbox without the label."""
        checked = index.model().data(index, QtCore.Qt.DisplayRole)
        check_box_style_option = QtGui.QStyleOptionButton()
        enabled = index.flags() & QtCore.Qt.ItemIsEnabled
        if enabled > 0:
            check_box_style_option.state |= QtGui.QStyle.State_Enabled
        else:
            check_box_style_option.state |= QtGui.QStyle.State_ReadOnly
        if checked:
            check_box_style_option.state |= QtGui.QStyle.State_On
        else:
            check_box_style_option.state |= QtGui.QStyle.State_Off
        check_box_style_option.rect = self.getCheckBoxRect(option)
        QtGui.QApplication.style().drawControl(
            QtGui.QStyle.CE_CheckBox, check_box_style_option, painter)

    def getCheckBoxRect(self, options):
        check_box_style_option = QtGui.QStyleOptionButton()
        check_box_rect = QtGui.QApplication.style().subElementRect(
            QtGui.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QtCore.QPoint(
            options.rect.x() + options.rect.width() / 2 - check_box_rect.width() / 2,
            options.rect.y() + options.rect.height() / 2 -
            check_box_rect.height() / 2)
        return QtCore.QRect(check_box_point, check_box_rect.size())

    def editorEvent(self, event, model, option, index):
        """Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses Key_Space or
        Key_Select and this cell is editable. Otherwise do nothing.
        """
        if not (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False
        if not (index.flags() & QtCore.Qt.ItemIsEnabled) > 0:
            return False

        def update_value():
            value = model.data(index)
            model.setData(index, not value)
            return True

        if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                return update_value()
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key_Space:
                return update_value()
        return False

    def createEditor(self, parent, option, index):
        """Create check box as our editor."""
        return None

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
