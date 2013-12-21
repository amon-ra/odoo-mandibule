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

from mandibule.views.workarea.dependency import DependencyContent
from mandibule.views.workarea.relation import RelationContent


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
        self.app.relation_ctl.execute_error.connect(self.execute_error)
        self.app.relation_ctl.finished.connect(self.relation_finished)
        self.app.dependency_ctl.updated.connect(self.dependency_updated)
        self.app.dependency_ctl.executed.connect(self.dependency_executed)
        self.app.dependency_ctl.execute_error.connect(self.execute_error)
        self.app.dependency_ctl.finished.connect(self.dependency_finished)
        self.tabCloseRequested.connect(self.close_tab)

    def relation_updated(self, id_):
        """Update title of the corresponding tab (if any)."""
        if id_ in self._tabs:
            data = self.app.relation_ctl.read(id_)
            sdata = self.app.server_ctl.read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(self._tabs[id_])
            self.setTabText(index, title)

    def relation_executed(self, id_):
        """Add/update a content when a relation graph is executed."""
        data = self.app.relation_ctl.read(id_)
        sdata = self.app.server_ctl.read(data['server_id'])
        title = "%s - %s" % (sdata['name'], data['name'])
        if id_ not in self._tabs:
            self._tabs[id_] = RelationContent(self.app, id_)
            self.addTab(self._tabs[id_], self.app.icons.icon_wait, title)
        else:
            index = self.indexOf(self._tabs[id_])
            self.setTabIcon(index, self.app.icons.icon_wait)
        self.setCurrentWidget(self._tabs[id_])

    def relation_finished(self, id_, data):
        """Update the tab icon when a relation graph is ready."""
        if id_ in self._tabs:
            index = self.indexOf(self._tabs[id_])
            self.setTabIcon(index, self.app.icons.icon_relation)

    def dependency_updated(self, id_):
        """Update title of the corresponding tab (if any)."""
        if id_ in self._tabs:
            data = self.app.dependency_ctl.read(id_)
            sdata = self.app.server_ctl.read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(self._tabs[id_])
            self.setTabText(index, title)

    def dependency_executed(self, id_):
        """Add/update a content when a module dependencies graph is executed."""
        data = self.app.dependency_ctl.read(id_)
        sdata = self.app.server_ctl.read(data['server_id'])
        title = "%s - %s" % (sdata['name'], data['name'])
        if id_ not in self._tabs:
            self._tabs[id_] = DependencyContent(self.app, id_)
            self.addTab(self._tabs[id_], self.app.icons.icon_wait, title)
        else:
            index = self.indexOf(self._tabs[id_])
            self.setTabIcon(index, self.app.icons.icon_wait)
        self.setCurrentWidget(self._tabs[id_])

    def dependency_finished(self, id_, data):
        """Update the tab icon when a module dependencies graph is ready."""
        if id_ in self._tabs:
            index = self.indexOf(self._tabs[id_])
            self.setTabIcon(index, self.app.icons.icon_dependencies)

    def execute_error(self, id_):
        """Close the tab if an error occurred during the execution."""
        index = self.indexOf(self._tabs[id_])
        self.close_tab(index)

    def close_tab(self, index):
        """Close a tab at the given `index`."""
        widget = self.widget(index)
        self.removeTab(index)
        widget.deleteLater()
        for id_, tab_content in self._tabs.iteritems():
            if tab_content == widget:
                del self._tabs[id_]
                break

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
