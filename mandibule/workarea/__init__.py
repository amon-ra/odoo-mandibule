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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
