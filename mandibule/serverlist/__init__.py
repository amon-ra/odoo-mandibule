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
import oerplib

from mandibule.serverlist.controlers.group import Group
from mandibule.serverlist.controlers.server import Server
from mandibule.serverlist.controlers.funcconfig import FuncConfig
from mandibule import config, modules
from mandibule.utils.i18n import _
from mandibule.serverlist import dialogs


class ServerListControler(object):
    def __init__(self, main_app):
        self.menu = None
        self._current_sel = None
        self._groups = []
        self.main_app = main_app
        self.widget = QtGui.QTreeWidget()
        self.widget.setHeaderHidden(True)
        self.widget.currentItemChanged.connect(self._cur_item)
        self.widget.itemDoubleClicked.connect(self._item_dblclick)
        self.widget.contextMenuEvent = self._context_menu
        for elt in config.CONFIG:
            self.add_group(Group(elt))

    def add_group(self, group):
        self.widget.addTopLevelItem(group.item)
        group.item.setExpanded(True)
        self._groups.append(group)

    def remove_group(self, group):
        windex = self.widget.indexOfTopLevelItem(group.item)
        self.widget.takeTopLevelItem(windex)
        self._groups.remove(group)

    def _save_config(self):
        config.save([group.serialize() for group in self._groups])

    def _cur_item(self, cur, prev):
        if cur:
            self._current_sel = cur.data(0, QtCore.Qt.UserRole)
        else:
            self._current_sel = None

    def _item_dblclick(self, item, col):
        if isinstance(self._current_sel, FuncConfig):
            self._exec_func()


    def _context_menu(self, event):
        if not self._current_sel:
            self.menu = QtGui.QMenu()
            self.menu.addAction(_("New group"), self._new_group)
        else:
            self.menu = self._current_sel.get_menu(self)
        if self.menu:
            self.menu.popup(event.globalPos())



    def _new_group(self):
        data, ok = dialogs.group_dialog()
        if ok:
            group = Group(data)
            config.add_group(group)
            self.add_group(group)
            self._save_config()

    def _edit_group(self):
        if isinstance(self._current_sel, Group):
            group = self._current_sel
        else:
            group = self._current_sel.group
        result, ok = dialogs.group_dialog(group)
        if ok:
            group.update(result)
            self._save_config()

    def _remove_group(self):
        if isinstance(self._current_sel, Group):
            groupdata = self._current_sel
        else:
            groupdata = self._current_sel.group
        self.remove_group(groupdata)
        self._save_config()

    def _new_server(self):
        if isinstance(self._current_sel, Group):
            group = self._current_sel
        else:
            group = self._current_sel.group
        result, ok = dialogs.server_dialog(self._groups, group=group)
        if ok:
            grp = result.pop('group')
            grp.add_server(Server(group, result))
            oerplib.tools.session.save(result['name'], result)
            self._save_config()


    def _edit_server(self):
        if isinstance(self._current_sel, Server):
            server = self._current_sel
        else:
            server = self._current_sel.server
        result, ok = dialogs.server_dialog(self._groups, server, server.group)
        if ok:
            grp = result.pop('group')
            if grp is not server.group:
                server.group.remove_server(server)
                grp.add_server(server)
                server.group = grp
            if server.name != result['name']:
                oerplib.tools.session.remove(server.name)
            server.update(result)
            oerplib.tools.session.save(result['name'], result)
            self._save_config()


    def _remove_server(self):
        if isinstance(self._current_sel, Server):
            server = self._current_sel
        else:
            server = self._current_sel.server
        server.group.remove_server(server)
        oerplib.tools.session.remove(server.name)
        self._save_config()

    def _new_func(self, mod_name, mod):
        def __wrapped():
            if isinstance(self._current_sel, Server):
                server = self._current_sel
            else:
                server = self._current_sel.server
            result, ok = mod.get_form().exec_()
            if ok:
                result['func_module'] = mod_name
                server.add_func_config(result)
                self._save_config()
        return __wrapped


    def _edit_func(self):
        mod_name = self._current_sel.func_module.name
        result, ok = modules.MODULES[mod_name].get_form(
            self._current_sel).exec_()
        if ok:
            self._current_sel.update(result)
            self._save_config()

    def _remove_func(self):
        self._current_sel.func_module.remove_config(self._current_sel)
        self._save_config()

    def _exec_func(self):
        self.main_app.workarea.add_result(self._current_sel)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
