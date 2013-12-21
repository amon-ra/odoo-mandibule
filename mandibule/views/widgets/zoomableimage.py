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
    def __init__(self, data=None):
        QtGui.QScrollArea.__init__(self)
        self._mt_prev_pos = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = None
        self.zoom_rate = 0.1    # Zoom in/out with a rate of 10%
        self.label = QtGui.QLabel(self)
        self.label.setScaledContents(True)
        self.setWidget(self.label)
        self.update_image(data)

    def wheelEvent(self, event):
        """Overloaded to zoom/unzoom the image when the Ctrl key is pressed."""
        if event.modifiers() & \
                QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
            if event.delta() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super(ZoomableImage, self).wheelEvent(event)

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

    def zoom_in(self):
        """Zoom in the image."""
        user_size = self.label.size()
        rate = (1 + self.zoom_rate)
        height = user_size.height() * rate
        width = user_size.width() * rate
        self.label.resize(width, height)

    def zoom_out(self):
        """Zoom out the image."""
        user_size = self.label.size()
        rate = (1 - self.zoom_rate)
        height = user_size.height() * rate
        width = user_size.width() * rate
        self.label.resize(width, height)

    def zoom_original(self):
        """Set the original size of the image."""
        real_size = self.pixmap.size()
        width, height = real_size.toTuple()
        self.label.resize(width, height)

    def zoom_fit_best(self):
        """Adjust zoom to fit the image to the parent widget size."""
        if self.parent():
            pixel_fix = 5   # Just to fit well in the parent widget
            real_width = self.pixmap.size().width() - pixel_fix
            real_height = self.pixmap.size().height() - pixel_fix
            parent_width = self.size().width() - pixel_fix
            parent_height = self.size().height() - pixel_fix
            height_rate = float(parent_height) / float(real_height)
            width_rate = float(parent_width) / float(real_width)
            # Give the priority to the height
            if height_rate < width_rate:
                width = real_width * height_rate
                self.label.resize(width, parent_height)
            # Or to the width
            else:
                height = real_height * width_rate
                self.label.resize(parent_width, height)

    def update_image(self, data=None):
        """Update the image with `data`."""
        if data:
            image = QtGui.QImage.fromData(data)
            self.pixmap = QtGui.QPixmap.fromImage(image)
        else:
            self.pixmap = QtGui.QPixmap()
        self.label.setPixmap(self.pixmap)
        self.zoom_original()
        self.label.update()
        self.update()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
