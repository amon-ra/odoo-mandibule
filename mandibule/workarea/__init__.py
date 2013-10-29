from PySide import QtGui


class WorkAreaController(object):
    def __init__(self, app):
        self.app = app
        self.widget = QtGui.QMdiArea()
