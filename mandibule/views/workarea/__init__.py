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

from mandibule.utils import zoomableimage


class WorkArea(QtGui.QTabWidget):
    """Workarea containing request results organized with tabs."""
    def __init__(self, app):
        QtGui.QTabWidget.__init__(self)
        self.app = app
        self._tabs = {}
        self.setTabsClosable(True)
        self.setMovable(True)
        self.app.relation_ctl.updated.connect(self.relation_updated)
        self.app.relation_ctl.executed.connect(self.relation_executed)
        self.app.relation_ctl.finished.connect(self.relation_finished)
        self.app.dependency_ctl.updated.connect(self.dependency_updated)
        self.app.dependency_ctl.executed.connect(self.dependency_executed)
        self.app.dependency_ctl.finished.connect(self.dependency_finished)
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBar().tabMoved.connect(self.move_tab)

    def _make_title(self, prefix, sdata, data):
        """Make and return a tab title."""
        return "%s %s - %s" % (prefix, sdata['name'], data['name'])

    def relation_updated(self, id_):
        """Update title of the corresponding tab (if any)."""
        if id_ in self._tabs:
            data = self.app.relation_ctl.read(id_)
            sdata = self.app.server_ctl.read(data['server_id'])
            title = self._make_title("[R]", sdata, data)
            index = self.indexOf(self._tabs[id_])
            self.setTabText(index, title)

    def relation_executed(self, id_, message):
        """Add/update a tab with `message` when a relation graph is executed."""
        data = self.app.relation_ctl.read(id_)
        sdata = self.app.server_ctl.read(data['server_id'])
        title = self._make_title("[R]", sdata, data)
        if id_ not in self._tabs:
            self._tabs[id_] = TabContent(self.app, id_)
            self.addTab(self._tabs[id_], title)
        self._tabs[id_].set_content(QtGui.QLabel(message))

    def relation_finished(self, id_, content):
        """Update a tab with `content` when a relation graph is ready."""
        content = zoomableimage.ZoomableImage(content[0]).widget
        self._tabs[id_].set_content(content)

    def dependency_updated(self, id_):
        """Update title of the corresponding tab (if any)."""
        if id_ in self._tabs:
            data = self.app.dependency_ctl.read(id_)
            sdata = self.app.server_ctl.read(data['server_id'])
            title = self._make_title("[D]", sdata, data)
            index = self.indexOf(self._tabs[id_])
            self.setTabText(index, title)

    def dependency_executed(self, id_, message):
        """Add/update a tab with `message` when a module dependencies graph
        is executed.
        """
        data = self.app.dependency_ctl.read(id_)
        sdata = self.app.server_ctl.read(data['server_id'])
        title = self._make_title("[R]", sdata, data)
        if id_ not in self._tabs:
            self._tabs[id_] = TabContent(self.app, id_)
            self.addTab(self._tabs[id_], title)
        self._tabs[id_].set_content(QtGui.QLabel(message))

    def dependency_finished(self, id_, content):
        """Update a tab with `content` when a module dependencies graph
        is ready.
        """
        content = zoomableimage.ZoomableImage(content[0]).widget
        self._tabs[id_].set_content(content)

    def close_tab(self, index):
        """Close a tab at the given `index`."""
        widget = self.widget(index)
        self.removeTab(index)
        widget.deleteLater()
        for id_, tab_content in self._tabs.iteritems():
            if tab_content == widget:
                del self._tabs[id_]
                break

    def move_tab(self, mfrom, mto):
        """Move a tab."""
        idx_from = self._server_windows[mfrom]
        idx_to = self._server_windows[mto]
        self._controlers[idx_from].index = mto
        self._controlers[idx_to].index = mfrom
        self._server_windows[mfrom], self._server_windows[mto] = \
                self._server_windows[mto], self._server_windows[mfrom]


class TabContent(QtGui.QWidget):
    """Content of a tab inside the workarea."""
    def __init__(self, app, id_):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.id_ = id_
        self.setLayout(QtGui.QVBoxLayout())

    def set_content(self, content):
        """Set the content of this tab."""
        # Remove the previous content
        for index in range(self.layout().count()):
            widget = self.layout().takeAt(index)
            widget.widget().deleteLater()
            del widget
        # Set the content and switch to its tab
        self.layout().addWidget(content)
        self.app.work_area.setCurrentWidget(self)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
