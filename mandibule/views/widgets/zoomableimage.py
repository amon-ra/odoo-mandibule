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
        self._mt_prev_pos = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = None
        self._zoom = 0
        self.label = QtGui.QLabel(self)
        self.label.setScaledContents(True)
        self.setWidget(self.label)
        self.update_image(data)

    def wheelEvent(self, event):
        """Overloaded to zoom/unzoom the image when the Ctrl key is pressed."""
        if event.modifiers() & \
                QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
            self.zoom(event.delta() / 120)
        else:
            super(ZoomableImage, self).wheelEvent(event)

    def keyPressEvent(self, event):
        """Overloaded to manage the zoom state with keyboard shortcuts."""
        if event.modifiers() & \
                QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
            if event.text() == '+':
                self.zoom(1)
            if event.text() == '-':
                self.zoom(-1)
            if event.text() == '0':
                self.zoom(10)
            if event.text() == '=':
                self.zoom_best()
        else:
            super(ZoomableImage, self).keyPressEvent(event)

    def mouseMoveEvent(self, event):
        """Overloaded to grab and scroll the image."""
        super(ZoomableImage, self).mouseMoveEvent(event)
        pos = event.pos()
        if self._mt_prev_pos:
            xdelta = self._mt_prev_pos.x() - pos.x()
            ydelta = self._mt_prev_pos.y() - pos.y()
            if abs(xdelta) < 100 and abs(ydelta) < 100:
                vsb = self.verticalScrollBar()
                hsb = self.horizontalScrollBar()
                vsb.setValue(vsb.value()+ydelta)
                hsb.setValue(hsb.value()+xdelta)
        self._mt_prev_pos = pos

    def zoom(self, zoom):
        """Resize the image according to the value of `zoom`."""
        self._zoom += zoom
        if self._zoom < 1:
            self._zoom = 1
        elif self._zoom > 10:
            self._zoom = 10
        size = self.pixmap.size()
        height = size.height() * self._zoom / 10
        width = size.width() * self._zoom / 10
        self.label.resize(width, height)

    def zoom_best(self):
        """Adjust zoom to fit the image to the window size."""
        img_size = self.pixmap.size()
        vp_size = self.size()
        height = float(vp_size.height())/float(img_size.height())
        width = float(vp_size.width())/float(img_size.width())
        ratio = min(img_size.width() * width, img_size.height() * height)
        self._zoom = ratio / 100
        self.zoom(0)

    def update_image(self, data):
        """Update the image with `data`."""
        image = QtGui.QImage.fromData(data)
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.label.setPixmap(self.pixmap)
        self.zoom(10)
        self.label.update()
        self.update()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
