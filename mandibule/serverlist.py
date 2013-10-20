from PySide import QtGui
from mandibule.controlers.serverlist import ServerListControler


class ServerList(QtGui.QTreeWidget):
    def __init__(self, parent):
        super(ServerList, self).__init__(parent.main_window)
        self.controler = ServerListControler(self, parent)
        self.setHeaderHidden(True)

    def contextMenuEvent(self, event):
        menu_data = self.currentItem().controler.menu()
        if not menu_data: 
            return
        menu = QtGui.QMenu(self)
        for label, action in menu_data:
            if label is not None:
                menu.addAction(label, action)
            else:
                menu.addSeparator()
        menu.popup(event.globalPos())

