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
import os.path
import json

from mandibule.utils import env


CONFIG_PATH = env.save_user_config_path('mandibule')

try:
    with open(os.path.join(CONFIG_PATH, 'config'), 'r') as fp:
        CONFIG = json.load(fp)
except IOError:
    CONFIG = []


def add_group(group):
    CONFIG.append(group.serialize())


def save(data):
    try:
        with open(os.path.join(CONFIG_PATH, 'config'), 'w') as fp:
            json.dump(data, fp, indent=4)
            CONFIG = data
            return True
    except IOError:
        return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
