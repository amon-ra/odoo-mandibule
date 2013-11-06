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
"""This module aims to provide functions helping the application to be
integrated with the system with some XDG helpers.

"""
import os
from xdg import BaseDirectory

def save_user_config_path(*resource):
    """Ensure $XDG_CONFIG_HOME/<resource>/ exists, and return its path.
    'resource' should normally be the name of your application. Use this
    when SAVING configuration settings. Use the ``load_user_config_path()``
    method for loading.

    """
    resource = resource or ['']
    return BaseDirectory.save_config_path(*resource)

def save_user_data_path(*resource):
    """Ensure $XDG_DATA_HOME/<resource>/ exists, and return its path.
    'resource' is the name of some shared resource. Use this when updating
    a shared (between programs) database. Use the ``load_user_data_path()``
    method for loading.

    """
    resource = resource or ['']
    return BaseDirectory.save_data_path(*resource)

def load_config_paths(*resource):
    """Returns a list which gives each directory named 'resource' in the
    configuration search path. Information provided by earlier directories
    should take precedence over later ones (ie, the user's config dir comes
    first).

    """
    resource = resource or ['']
    return [res for res in BaseDirectory.load_config_paths(*resource)]
    #return [os.path.join(path, 'mounty', *resource)
    #        for path in BaseDirectory.xdg_config_dirs]
#print 'load_config_paths', load_config_paths()

def load_user_config_path(*resource):
    return os.path.join(BaseDirectory.xdg_config_home, *resource)
#print 'load_user_config_path', load_user_config_path()

def load_data_paths(*resource):
    """Returns a list which gives each directory named 'resource' in the
    shared data search path. Information provided by earlier directories should
    take precedence over later ones (ie, the user's data dir comes
    first).

    """
    resource = resource or ['']
    return [res for res in BaseDirectory.load_data_paths(*resource)]
    #return [os.path.join(path, 'mounty', *resource)
    #        for path in BaseDirectory.xdg_data_dirs]
#print 'load_data_paths', load_data_paths()
#print 'load_data_paths', load_data_paths('icons', 'hicolor', '16x16',
#                                         'apps', 'mounty.png')

def load_user_data_path(*resource):
    return os.path.join(BaseDirectory.xdg_data_home, *resource)
#print 'load_user_data_path', load_user_data_path()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
