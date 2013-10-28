from PySide import QtGui, QtCore
from mandibule.controlers.group import Group
from mandibule.controlers.server import Server
from mandibule.controlers.funcconfig import FuncConfig
from mandibule import config, modules
from mandibule.utils.i18n import _
from mandibule.utils import dialogs
import oerplib

class ServerListControler(object):
    def __init__(self, main_app):
        self._current_sel = None
        self._groups = []
        self.main_app = main_app
        self.widget = QtGui.QTreeWidget()
        self.widget.setHeaderHidden(True)
        self.widget.currentItemChanged.connect(self._cur_item)
        self.widget.contextMenuEvent = self._context_menu
        for elt in config.CONFIG:
            self.add_group(Group(elt))

    def add_group(self, group):
        self.widget.addTopLevelItem(group.item)
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

    def _context_menu(self, event):
        self.menu = QtGui.QMenu()
        group_menu = QtGui.QMenu(_("Groups"))
        self.menu.addMenu(group_menu)
        group_menu.addAction(_("New group"), self._new_group)
        if self._current_sel:
            group_menu.addAction(_("Edit group"), self._edit_group)
            group_menu.addAction(_("Remove group"), self._remove_group)
            serv_menu = QtGui.QMenu(_("Server"))
            self.menu.addMenu(serv_menu)
            serv_menu.addAction(_("New server"), self._new_server)
            if not isinstance(self._current_sel, Group):
                serv_menu.addAction(_("Edit server"), self._edit_server)
                serv_menu.addAction(_("Remove server"), self._remove_server)
                func_menu = QtGui.QMenu(_("Functions"))
                self.menu.addMenu(func_menu)
                new_func_menu = QtGui.QMenu(_("New function"))
                func_menu.addMenu(new_func_menu)
                for mod_name, mod in modules.MODULES:
                    new_func_menu.addAction(mod_name,
                            self._new_func(mod_name, mod))

                if isinstance(self._current_sel, FuncConfig):
                    func_menu.addAction(_("Edit function"), self._edit_func)
                    func_menu.addAction(_("Remove function"),
                            self._remove_func)
                    func_menu.addSeparator()
                    func_menu.addAction(_("Execute function"), self._exec_func)
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
            group= self._current_sel
        else:
            group= self._current_sel.group
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
        config = self._current_sel
        mod_name = self._current_sel.func_module.name
        result, ok = modules.MODULES[mod_name].get_form(config)
        if ok:
            self._current_sel.update(result)
            self._save_config()

    def _remove_func(self):
        self._current_sel.func_module.remove_config(self._current_sel)
        self._save_config()

    def _exec_func(self):
        func_mod = modules.get_module(self._current_sel.func_module.name)
        func_mod.execute(self._current_sel)
