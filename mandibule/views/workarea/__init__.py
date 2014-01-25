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
import uuid

from PySide import QtGui, QtCore

from mandibule.utils.i18n import _
from mandibule.views.workarea.dependency import DependencyContent
from mandibule.views.workarea.relation import RelationContent
from mandibule.views.widgets import dialog


class WorkArea(QtGui.QTabWidget):
    """Workarea containing request results organized with tabs."""

    def __init__(self, app):
        QtGui.QTabWidget.__init__(self)
        self.app = app
        self.tabs = {}         # Identify persistent functions
        self.tabs_tmp = {}     # Identify temporary functions
        self.setTabsClosable(True)
        self.setMovable(True)
        for ctl in ['relation_ctl', 'dependency_ctl']:
            getattr(self.app, ctl).created.connect(self.function_saved)
            getattr(self.app, ctl).deleted.connect(self.function_deleted)
            getattr(self.app, ctl).updated.connect(self.function_updated)
            getattr(self.app, ctl).executed.connect(self.function_executed)
            getattr(self.app, ctl).finished.connect(self.function_finished)
        self.tabCloseRequested.connect(self.close_tab)
        # Shortcuts
        action_close = QtGui.QAction(self)
        action_close.setShortcut(QtGui.QKeySequence.Close)
        action_close.triggered.connect(
            lambda: self.close_tab(self.currentIndex()))
        self.addAction(action_close)
        action_prev = QtGui.QAction(self)
        action_prev.setShortcut(QtGui.QKeySequence.SelectPreviousPage)
        action_prev.triggered.connect(
            lambda: self.setCurrentIndex(self.currentIndex() - 1))
        self.addAction(action_prev)
        action_next = QtGui.QAction(self)
        action_next.setShortcut(QtGui.QKeySequence.SelectNextPage)
        action_next.triggered.connect(
            lambda: self.setCurrentIndex(self.currentIndex() + 1))
        self.addAction(action_next)

    def new_function(self, server_id, context):
        """Add a new relation tab which can be saved later."""
        sdata = self.app.server_ctl.read(server_id)
        title = u"%s - %s" % (sdata['name'], _(u"New"))
        id_tmp = uuid.uuid4().hex
        if context.get('model') == 'relation':
            self.tabs_tmp[id_tmp] = RelationContent(
                self.app, server_id, id_tmp, new=True)
            self.addTab(
                self.tabs_tmp[id_tmp], self.app.icons.icon_relation, title)
        if context.get('model') == 'dependency':
            self.tabs_tmp[id_tmp] = DependencyContent(
                self.app, server_id, id_tmp, new=True)
            self.addTab(
                self.tabs_tmp[id_tmp], self.app.icons.icon_dependencies, title)
        self.tabs_tmp[id_tmp].data_changed.connect(self.function_unsaved)
        self.tabs_tmp[id_tmp].data_restored.connect(self.function_restored)
        self.tabs_tmp[id_tmp].show_panel()
        self.setCurrentWidget(self.tabs_tmp[id_tmp])

    def edit_function(self, id_, context):
        """Open an existing function to edit it."""
        if context.get('model') == 'relation':
            ctl = self.app.relation_ctl
            data = ctl.read(id_)
            ContentClass = RelationContent
            icon = self.app.icons.icon_relation
        if context.get('model') == 'dependency':
            ctl = self.app.dependency_ctl
            data = ctl.read(id_)
            ContentClass = DependencyContent
            icon = self.app.icons.icon_dependencies
        sdata = self.app.server_ctl.read(data['server_id'])
        title = "%s - %s" % (sdata['name'], data['name'])
        if id_ not in self.tabs:
            content = ContentClass(self.app, data['server_id'], id_)
            content.data_changed.connect(self.function_unsaved)
            content.data_restored.connect(self.function_restored)
            self.tabs[id_] = content
            self.addTab(self.tabs[id_], icon, title)
        self.tabs[id_].show_panel()
        self.setCurrentWidget(self.tabs[id_])

    def function_saved(self, id_, data, context):
        """Update title of the corresponding tab when a function is saved."""
        from_id_tmp = context.get('from_id_tmp')
        if from_id_tmp:
            content = self.tabs_tmp.pop(from_id_tmp)
            self.tabs[id_] = content
            sdata = self.app.server_ctl.read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def function_unsaved(self, id_, data):
        """Update title of the corresponding tab when function data
        has been changed.
        """
        content = self.tabs.get(id_)
        if content and content.unsaved:
            sdata = self.app.server_ctl.read(data['server_id'])
            title = "%s - %s*" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def function_restored(self, id_, data):
        """Update title of the corresponding tab when function data
        has been restored.
        """
        content = self.tabs.get(id_)
        if content and not content.unsaved:
            sdata = self.app.server_ctl.read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def function_deleted(self, id_, context):
        """Update title of the corresponding tab when a function is deleted."""
        if id_ in self.tabs:
            content = self.tabs.pop(id_)
            self.tabs_tmp[id_] = content
            sdata = self.app.server_ctl.read(content.server_id)
            title = "%s - %s" % (sdata['name'], _(u"New"))
            index = self.indexOf(content)
            self.setTabText(index, title)

    def function_updated(self, id_, data, context):
        """Update title of the corresponding tab when a function is updated."""
        content = self.tabs.get(id_)
        if content:
            sdata = self.app.server_ctl.read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def function_executed(self, id_, data, context):
        """Update title of the corresponding tab when a function is executed."""
        content = self.tabs.get(id_) or self.tabs_tmp.get(id_)
        if content:
            index = self.indexOf(content)
            self.setTabIcon(index, self.app.icons.icon_wait)
            self.setCurrentWidget(content)

    def function_finished(self, id_, data, context):
        """Update the tab icon when a function is ready."""
        if context.get('model') == 'relation':
            icon = self.app.icons.icon_relation
        if context.get('model') == 'dependency':
            icon = self.app.icons.icon_dependencies
        content = self.tabs.get(id_) or self.tabs_tmp.get(id_)
        if content:
            index = self.indexOf(content)
            self.setTabIcon(index, icon)

    def close_tab(self, index):
        """Close a tab at the given `index`."""
        widget = self.widget(index)
        close = True
        if widget.unsaved:
            close = dialog.confirm(
                self,
                _(u"This function has been modified. Close anyway?"),
                _(u"Modified function"))
        if close:
            self.removeTab(index)
            widget.deleteLater()
            for id_, tab_content in self.tabs.iteritems():
                if tab_content == widget:
                    del self.tabs[id_]
                    break
            for id_, tab_content in self.tabs_tmp.iteritems():
                if tab_content == widget:
                    del self.tabs_tmp[id_]
                    break

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
