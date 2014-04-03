# -*- coding: UTF-8 -*-
##############################################################################
#
#    Mandibule, an explorer for OpenERP servers
#    Copyright (C) 2014 Sébastien Alix
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
"""This package contains modules of the application.
A module can declare all kind of stuff to register inside the application, such
as controllers, actions, menus... and so on.

When executed, the ``load`` function handle the registration of module contents.
"""
import os
import imp
import inspect

from mandibule.reg import controller, icon, action, tree, ui

# Default addons path
ADDONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'addons')


def register(app):
    """Load/register addons."""
    # Scan addons (import the 'base' module first)
    modules_path = [('base', os.path.join(ADDONS_PATH, 'base'))]
    for file_name in os.listdir(ADDONS_PATH):
        if file_name == 'base':
            continue
        directory = os.path.join(ADDONS_PATH, file_name)
        if os.path.isdir(directory):
            modules_path.append((file_name, directory))
    print("LOADING MODULES:")
    for name, module_path in modules_path:
        try:
            file_, path, desc = imp.find_module(name, [ADDONS_PATH])
        except ImportError:
            print("\t'%s' is not a module. Skipping." % module_path)
        else:
            imp.load_module(module_path, file_, path, desc)
            print("\t+ %s" % name)
    # Load controllers
    for name in controller.ControllerRegister.__classes__:
        class_ = controller.ControllerRegister.__classes__[name]
        class_(app)
    # Load icons
    for name in icon.IconsRegister.__classes__:
        class_ = icon.IconsRegister.__classes__[name]
        class_(app)
    # Load actions
    for name in action.ActionRegister.__classes__:
        class_ = action.ActionRegister.__classes__[name]
        class_(app)
    # Load UI
    ui.UIRegister.__classes__['main_window'](app)


def connect():
    """Connect objects considered as singletons to Qt signals of widgets
    composing the application.
    This method is called by the application once all widgets are instanciated,
    to ensure the registration of signal connections.
    """
    for name in action.Action:
        action.Action[name].__connect__()
    for ui_part in ui.UI:
        ui_part = ui.UI[ui_part]
        ui_part.__connect__()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
