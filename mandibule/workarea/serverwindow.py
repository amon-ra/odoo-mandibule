from PySide import QtGui

class ServerWindow(object):
    def __init__(self, parent, server):
        self.server = server
        self.parent = parent

        self.widget = QtGui.QTabWidget()

        self.results = []

    def add_result(self, res_name, res_widget):
        print res_name, res_widget
        if res_name not in self.results:
            self.results.append(res_name)
            self.widget.addTab(res_widget, res_name)
            self.widget.insertTab(index, res_widget, res_name)

