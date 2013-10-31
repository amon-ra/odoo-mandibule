from PySide import QtGui, QtCore
from mandibule.serverlist.controlers.funcmodule import FuncModule
from mandibule.serverlist.controlers.funcconfig import FuncConfig
from mandibule.utils.i18n import _
from mandibule import modules


class Server(object):
    def __init__(self, group, data):
        self.group = group
        self.name = data['name']
        self.funcs = {}
        self.item = QtGui.QTreeWidgetItem()
        self.item.setText(0, self.name)
        self.item.setData(0, QtCore.Qt.UserRole, self)
        for func, configs in data.get('funcs', {}).items():
            self.add_func_module(FuncModule(self.group, self, func, configs))


    def add_func_module(self, func_module):
        self.item.addChild(func_module.item)
        self.funcs[func_module.name] = func_module

    def remove_func_module(self, func_module):
        if not self.funcs[func_module.configs]:
            self.item.removeChild(func_module.item)
            del self.funcs[func_module.name]

    def add_func_config(self, func_config):
        if func_config['func_module'] not in self.funcs:
            self.add_func_module(FuncModule(
                self.group,
                self,
                func_config.pop('func_module'),
                [func_config]))
        else:
            funcmod = self.funcs[func_config['func_module']]
            funcmod.add_config(
                    FuncConfig(self.group, self, funcmod, func_config)
                    )

    def update(self, data):
        self.name = data['name']
        self.item.setText(0, self.name)

    def serialize(self):
        out = {'name': self.name}
        funcs = getattr(self, 'funcs', False)
        if funcs:
            out['funcs'] = {}
            for func, ctrl in funcs.items():
                out['funcs'][func] = [conf.serialize() for conf in \
                        ctrl.configs.values()]
        return out

    def get_menu(self, ref):
        menu = QtGui.QMenu(ref.widget)
        menu.addAction(_("Edit server"), ref._edit_server)
        menu.addAction(_("Remove server"), ref._remove_server)
        menu.addSeparator()
        for mod_name, mod in modules.MODULES:
            menu.addAction(
                    _("New %s") % mod_name,
                    ref._new_func(mod_name, mod))
        return menu

