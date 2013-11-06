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

from mandibule.serverlist.controlers.funcconfig import FuncConfig


class FuncModule(object):
    def __init__(self, group, server, name, configs):
        self.group = group
        self.server = server
        self.name = name
        self.configs = {}
        self.item = QtGui.QTreeWidgetItem()
        self.item.setText(0, self.name)
        self.item.setData(0, QtCore.Qt.UserRole, self)
        for config in configs:
            self.add_config(FuncConfig(self.group, self.server, self, config))


    def add_config(self, config):
        self.configs[config.name] = config
        self.item.addChild(config.item)

    def remove_config(self, config):
        self.item.removeChild(config.item)
        del self.configs[config.name]

    def get_menu(self, ref):
        #TODO
        return None

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
