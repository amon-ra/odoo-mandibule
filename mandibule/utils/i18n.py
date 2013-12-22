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
    lang, coding = locale.getdefaultlocale()
    for localedir_ in env.load_data_paths():
        try:
            dir_ = os.path.join(localedir_, 'locale', lang)
            return gettext.translation(
                    'mandibule',
                    localedir = dir_,
                    languages = lang).ugettext
        except Exception, e:
            #print dir_, lang
            pass

    return lambda x: x

_ = _get_trans()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
