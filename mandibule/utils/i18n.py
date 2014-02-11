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
import locale, gettext, os

from mandibule.utils import env


def _get_trans():
    """Try to found the corresponding locale to use for translations."""
    lang = locale.getdefaultlocale()[0]
    for datadir in env.load_data_paths():
        try:
            path = None
            ldir1 = os.path.join(datadir, 'locale', lang)
            ldir2 = os.path.join(datadir, lang)
            # Try with 'locale' sufix
            if os.path.exists(ldir1):
                path = ldir1
            # Try without the sufix (especially for the ./build/mo/ directory
            # used in development which does not contain a 'locale'
            # sub-directory)
            elif os.path.exists(ldir2):
                path = ldir2
            if path:
                return gettext.translation(
                    'mandibule',
                    localedir=path,
                    languages=lang).ugettext
        except IOError:
            pass

    return lambda x: x

_ = _get_trans()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
