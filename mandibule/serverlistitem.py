from PySide import QtGui

class ServerListItem(QtGui.QTreeWidgetItem):
    def __init__(self, controler, text):
        super(ServerListItem, self).__init__()
        self.setText(0, text)
        self.controler = controler


