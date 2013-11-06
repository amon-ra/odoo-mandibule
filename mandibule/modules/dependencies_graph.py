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
import oerplib

from mandibule.utils.form import FormDialog, TextField, BoolField
from mandibule.utils.i18n import _
from mandibule.utils import zoomableimage
from mandibule.workarea import WorkAreaResultItem


def _clean(data):
    return [s.strip().encode('utf8') for s in data.split()]


def get_form(config=None):
    defaults = getattr(config, 'data', {})
    return FormDialog((
            (
                'name',
                TextField(
                    _("Name"),
                    defaults.get('name', '')
                    )
                ),
            (
                'modules',
                TextField(
                    _("Modules"),
                    defaults.get('modules', ''),
                    multi=True
                    )
                ),
            (
                'models',
                TextField(
                    _("Models"),
                    defaults.get('models', ''),
                    multi=True
                    )
                ),
            (
                'blacklist',
                TextField(
                    _("Blacklist"),
                    defaults.get('blacklist', ''),
                    multi=True
                    )
                ),
            (
                'restrict',
                BoolField(
                    _("Restrict"),
                    defaults.get('restrict', False)
                    )
                )
            ))


def execute(config):
    modules = _clean(config.data['modules'])
    models = _clean(config.data['models'])
    blacklist = _clean(config.data['blacklist'])
    oerp = oerplib.OERP.load(config.server.name)
    dependencies = oerp.inspect.dependencies(
            modules,
            models,
            blacklist,
            config.data['restrict'])
    graph = dependencies.make_dot().create_png()
    out = zoomableimage.ZoomableImage(graph)
    return WorkAreaResultItem(config.server.name, config.name, out)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
