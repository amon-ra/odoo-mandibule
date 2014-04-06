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
"""Defines the workbook."""
import uuid

from PySide import QtGui

from mandibule.reg import Controller, WorkArea, Icons, UI
from mandibule.utils.i18n import _
from mandibule.widgets import dialog


class WorkBook(UI, QtGui.QTabWidget):
    """Contains work areas organized with tabs."""
    __metadata__ = {
        'name': 'workbook',
    }

    def __init__(self, app):
        UI.__init__(self, app)
        QtGui.QTabWidget.__init__(self)
        self.tabs = {}         # Identify persistent functions
        self.tabs_tmp = {}     # Identify temporary functions
        self.setTabsClosable(True)
        self.setMovable(True)
        for name in Controller:
            ctl = Controller[name]
            if ctl.__metadata__.get('function'):
                ctl.deleted.connect(self._function_deleted)
                ctl.updated.connect(self._function_updated)
                ctl.executed.connect(self._function_executed)
                ctl.finished.connect(self._function_finished)
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

    def new_function(self, model, server_id):
        """Add a new workarea which can be saved later."""
        sdata = Controller['server'].read(server_id)
        title = u"%s - %s" % (sdata['name'], _(u"New"))
        id_tmp = uuid.uuid4().hex
        self.tabs_tmp[id_tmp] = WorkArea[model](
            self.app, server_id, id_tmp, new=True)
        self.addTab(self.tabs_tmp[id_tmp], Icons[model], title)
        self.tabs_tmp[id_tmp].created.connect(self._function_created)
        self.tabs_tmp[id_tmp].data_changed.connect(self._function_unsaved)
        self.tabs_tmp[id_tmp].data_restored.connect(self._function_restored)
        self.tabs_tmp[id_tmp].show_panel()
        self.setCurrentWidget(self.tabs_tmp[id_tmp])

    def edit_function(self, model, id_):
        """Open an existing function to edit it."""
        ctl = Controller[model]
        data = ctl.read(id_)
        ContentClass = WorkArea[model]
        icon = Icons[model]
        sdata = Controller['server'].read(data['server_id'])
        title = "%s - %s" % (sdata['name'], data['name'])
        if id_ not in self.tabs:
            content = ContentClass(self.app, data['server_id'], id_)
            content.data_changed.connect(self._function_unsaved)
            content.data_restored.connect(self._function_restored)
            self.tabs[id_] = content
            self.addTab(self.tabs[id_], icon, title)
        self.tabs[id_].show_panel()
        self.setCurrentWidget(self.tabs[id_])

    def _function_created(self, model, id_tmp, id_):
        """Switch the context identified by a old temporary ID to the new one
        when a function is saved for the first time.
        """
        content = self.tabs_tmp.pop(id_tmp)
        self.tabs[id_] = content
        data = Controller[model].read(id_)
        sdata = Controller['server'].read(data['server_id'])
        title = "%s - %s" % (sdata['name'], data['name'])
        index = self.indexOf(content)
        self.setTabText(index, title)

    def _function_unsaved(self, model, id_, data):
        """Update title of the corresponding tab when function data
        has been changed.
        """
        content = self.tabs.get(id_)
        if content and content.unsaved:
            sdata = Controller['server'].read(data['server_id'])
            title = "%s - %s*" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def _function_restored(self, model, id_, data):
        """Update title of the corresponding tab when function data
        has been restored.
        """
        content = self.tabs.get(id_)
        if content and not content.unsaved:
            sdata = Controller['server'].read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def _function_deleted(self, model, id_):
        """Update title of the corresponding tab when a function is deleted."""
        if id_ in self.tabs:
            content = self.tabs.pop(id_)
            self.tabs_tmp[id_] = content
            sdata = Controller['server'].read(content.server_id)
            title = "%s - %s" % (sdata['name'], _(u"New"))
            index = self.indexOf(content)
            self.setTabText(index, title)

    def _function_updated(self, model, id_, data):
        """Update title of the corresponding tab when a function is updated."""
        content = self.tabs.get(id_)
        if content:
            sdata = Controller['server'].read(data['server_id'])
            title = "%s - %s" % (sdata['name'], data['name'])
            index = self.indexOf(content)
            self.setTabText(index, title)

    def _function_executed(self, model, id_, data):
        """Update title of the corresponding tab when a function is executed."""
        content = self.tabs.get(id_) \
            or self.tabs_tmp.get(id_)
        if content:
            index = self.indexOf(content)
            self.setTabIcon(index, Icons['wait'])
            self.setCurrentWidget(content)

    def _function_finished(self, model, id_, data):
        """Update the tab icon when a function is ready."""
        icon = Icons[model]
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
