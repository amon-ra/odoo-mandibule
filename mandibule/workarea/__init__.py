from PySide import QtGui

class WorkAreaResultItem(object):
    def __init__(self, server, func_name, res_widget):
        self.server = server
        self.func_name = func_name
        self.widget = res_widget

class WorkAreaController(object):
    def __init__(self, app):
        self.app = app
        self.widget = QtGui.QTabWidget()
        self.widget.setTabsClosable(True)
        self.widget.setMovable(True)
        self.widget.tabCloseRequested.connect(self.close_tab)
        self.widget.tabBar().tabMoved.connect(self.move_tab)
        self._server_windows = []

    def add_result(self, result_item):
        item_controler = result_item.widget
        title = '%s/%s' % (result_item.server, result_item.func_name)
        if title not in self._server_windows:
            self._server_windows.append(title)
            self.widget.addTab(item_controler.widget, title)
        else:
            index = self._server_windows.index(title)
            self.widget.removeTab(index)
            self.widget.insertTab(index, item_controler.widget, title)
        self.widget.setCurrentIndex(self._server_windows.index(title))

    def close_tab(self, index):
        self.widget.removeTab(index)
        del self._server_windows[index]

    def move_tab(self, mfrom, mto):
        self._server_windows[mfrom], self._server_windows[mto] = \
                self._server_windows[mto], self._server_windows[mfrom]
