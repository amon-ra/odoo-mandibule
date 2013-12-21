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
"""Initialize the database and insert default values in the database during
the first launch of the application.
"""
import os.path

from mandibule import db
from mandibule.utils.i18n import _
from mandibule.controllers import GroupController


def init(app):
    """Insert default data if the database is empty (first launch)."""
    if not db.read():
        # Default server group
        app.group_ctl.create({'name': _(u"Servers")})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
