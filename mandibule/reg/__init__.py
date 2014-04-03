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
"""Contains all classes and tools used to register controllers, actions, views
and any elements that a module can bring to the application.
"""
from PySide.QtCore import QObject

__all__ = [
    'Controller',
    'Icons',
]


class Register(type(QObject), type):
    """Base metaclass to define a register."""

    def __new__(mcs, name, bases, attrs):
        if not hasattr(mcs, '__classes__'):
            mcs.__classes__ = {}
        if not hasattr(mcs, '__objects__'):
            if mcs._objects:
                mcs.__objects__ = {}
            else:
                mcs.__objects__ = []
        class_ = super(Register, mcs).__new__(
            mcs, name, bases, attrs)
        if class_.__metadata__.get('name'):
            mcs.__classes__[class_.__metadata__['name']] = class_
        return class_

    def add(mcs, obj):
        """Add the object `obj` to the register."""
        raise NotImplementedError


class MultiRegister(Register):
    """Metaclass to register classes which will have several instances."""
    _objects = False

    def __getitem__(mcs, name):
        return mcs.__classes__[name]

    def __iter__(mcs):
        return iter(mcs.__classes__)

    def __len__(mcs):
        return len(mcs.__classes__)

    def add(mcs, obj):
        mcs.__objects__.append(obj)


class SingleRegister(Register):
    """Metaclass to register classes which will have only one instance."""
    _objects = True

    def __getitem__(mcs, name):
        return mcs.__objects__[name]

    def __iter__(mcs):
        return iter(mcs.__objects__)

    def __len__(mcs):
        return len(mcs.__objects__)

    def add(mcs, obj):
        mcs.__objects__[obj.__metadata__['name']] = obj


class Element(object):
    """Base class to implement a new element."""

    def __init__(self, app):
        self.app = app
        self.__metaclass__.add(self.__class__, self)

    def __connect__(self):
        """Signals connection to other widgets of the application
        should be made in this method.
        """
        pass


class Single(Element):
    """Base class to implement a "singleton" element."""

    def __init__(self, app):
        super(Single, self).__init__(app)


class Multi(Element):
    """Base class to implement a class which aims to be instancied
    several times.
    """

    def __init__(self, app):
        super(Multi, self).__init__(app)
        self.__connect__()


from .controller import Controller
from .icon import Icons

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
