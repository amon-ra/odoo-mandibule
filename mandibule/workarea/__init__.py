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
from mandibule import modules

class ThreadFunc(QtCore.QThread):
    result_ready = QtCore.Signal(tuple)
    def __init__(self, func, *args, **kwargs):
        super(ThreadFunc, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.result_ready.emit(result)

class FuncWidgetControler(object):
    def __init__(self, workarea, data):
        self.workarea = workarea
        self.initialized = False
        self.data = data
        self.running = False
        self.pending_data = None
        self.thread = None
        self.widgetCtrl = None
        self.title = '%s - %s' % (data.server.name, data.name)
        self.index = self.workarea.get_index()
        self._widget = QtGui.QWidget()
        self._layout = QtGui.QVBoxLayout()
        self._widget.setLayout(self._layout)
        self._inner_widget = QtGui.QLabel('Running...')

    def render(self, data=None):
        if not self.initialized:
            self.initialized = True
            self._layout.addWidget(self._inner_widget)
            self.workarea.widget.addTab(self._widget, self.title)
            self.workarea.widget.setCurrentIndex(self.index)
        if data:
            if not self.running:
                self.data = data
            else:
                self.pending_data = data
                return
        mod = modules.get_module(self.data.func_module.name)
        self.running = True
        self.thread = ThreadFunc(mod.execute, self.data)
        self.thread.result_ready.connect(self.finalize)
        self.thread.finished.connect(self._finished)
        self.thread.start()

    def finalize(self, result):
        if not self.pending_data:
            widget_ctrl, wdata = result
            self.widgetCtrl = widget_ctrl(wdata)
            self._layout.removeWidget(self._inner_widget)
            self._layout.addWidget(self.widgetCtrl.widget)
            self._inner_widget = self.widgetCtrl.widget
            '''
            self.workarea.widget.removeTab(self.index)
            self.workarea.widget.insertTab(
                    self.index,
                    self.widgetCtrl.widget,
                    self.title)
            '''

    def _finished(self):
        self.running = False
        if self.pending_data:
            data = self.pending_data
            self.pending_data = None
            self.render(data)

class WorkAreaController(object):
    def __init__(self, app):
        self.app = app
        self.widget = QtGui.QTabWidget()
        self.widget.setTabsClosable(True)
        self.widget.setMovable(True)
        self.widget.tabCloseRequested.connect(self.close_tab)
        self.widget.tabBar().tabMoved.connect(self.move_tab)
        self._server_windows = []
        self._controlers = {}
        self._trash = []

    def get_index(self):
        return len(self._server_windows)

    def add_result(self, item):
        controler = FuncWidgetControler(self, item)
        if controler.title not in self._server_windows:
            self._server_windows.append(controler.title)
            self._controlers[controler.title] = controler
            controler.render()
        else:
            self._controlers[controler.title].render(item)

    def close_tab(self, index):
        self.widget.removeTab(index)
        title = self._server_windows[index]
        controler = self._controlers[title]
        if controler.running:
            self._trash.append(controler)
        del self._server_windows[index]
        del self._controlers[title]

    def move_tab(self, mfrom, mto):
        idx_from = self._server_windows[mfrom]
        idx_to = self._server_windows[mto]
        self._controlers[idx_from].index = mto
        self._controlers[idx_to].index = mfrom
        self._server_windows[mfrom], self._server_windows[mto] = \
                self._server_windows[mto], self._server_windows[mfrom]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
