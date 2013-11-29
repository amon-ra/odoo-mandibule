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


class ZoomableImage(QtGui.QScrollArea):
    """Widget containing an image on which zoom in/out operations
    can be performed.
    """
    def __init__(self, data):
        QtGui.QScrollArea.__init__(self)
        self.image = QtGui.QImage.fromData(data)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.label = QtGui.QLabel()
        self.label.setScaledContents(True)
        self.label.setPixmap(self.pixmap)
        self.setWidget(self.label)
        self.label.wheelEvent = self.wheelEvent
        self._zoom = 10

    def wheelEvent(self, event):
        if event.modifiers() & \
                QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
            self._zoom += (event.delta() / 120)
            if self._zoom < 1:
                self._zoom = 1
            elif self._zoom > 10:
                self._zoom = 10
            size = self.image.size()
            height = size.height() * self._zoom / 10
            width = size.width() * self._zoom / 10
            self.label.resize(width, height)
        else:
            event.accept()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
