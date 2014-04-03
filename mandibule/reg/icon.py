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
"""Supply the `Icons` base class and manage the registration of
icons with the `IconsRegister` class.
"""
from . import SingleRegister, Single


class IconsRegister(SingleRegister):
    """Metaclass which register icons."""
    pass


class Icons(object):
    """Base class to load icons."""
    __metaclass__ = IconsRegister
    __metadata__ = {
        'name': None,
    }

    def __init__(self, app):
        self.app = app
        # Generate and register icons
        for name, qicon in self.generate().iteritems():
            self.__metaclass__.__objects__[name] = qicon

    def generate(self):
        """Return a collection of icons::

            >>> icons.generate()
            {'server': <PySide.QtGui.QIcon object at 0x2633bd8>}
        """
        raise NotImplementedError

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
