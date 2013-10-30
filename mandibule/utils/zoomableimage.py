from PySide import QtGui, QtCore

class ZoomableImage(object):
    def __init__(self, data):
        self.image = QtGui.QImage.fromData(data)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.label = QtGui.QLabel()
        self.label.setScaledContents(True)
        self.label.setPixmap(self.pixmap)
        self.widget = QtGui.QScrollArea()
        self.widget.setWidget(self.label)
        self.label.wheelEvent = self.wheelEvent
        self._zoom = 10

    def wheelEvent(self, event):
        if event.modifiers() & \
                QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
            self._zoom += event.delta()/120
            if self._zoom < 1:
                self._zoom = 1
            elif self._zoom > 10:
                self._zoom = 10
            size = self.image.size()
            height = size.height() * self._zoom / 10
            width = size.width() * self._zoom / 10
            self.label.resize(width, height)
        else:
            event.ignore()
