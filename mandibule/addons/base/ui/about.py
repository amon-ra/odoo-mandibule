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
"""About dialog box."""
from PySide import QtGui

from mandibule.reg import UI
from mandibule import __version__
from mandibule.utils.i18n import _

TEMPLATE = u"""
<center>
<h2>{subtitle}</h2>
<p><a href="http://mandibule.bitbucket.org">http://mandibule.bitbucket.org</a></p>
<p>{p1}</p>
<p>{p2}</p>
<p>{p3}</p>
<p style="font-size: 8pt;">Copyright &copy; 2013-2014 Sébastien Alix<br/>
Copyright &copy; 2013-2014 Frédéric Fidon</p>
<p>{p4}</p>
</center>
"""

TITLE = _(u"About Mandibule")
SUBTITLE = _(u"Mandibule") + " {0}".format(__version__)
P1 = _(u"Mandibule is a graphical tool to explore data of OpenERP servers, "
       u"helping developpers to quickly obtain useful information.")
P2 = _(u"It is developped in Python, and relies on the "
       u"<a href='http://pythonhosted.org/OERPLib/'>OERPLib</a> library.")
P3 = _(u"This software is available under the GNU General Public "
       u"License v3.0.")
P4 = _(u"For any suggestions or bugs, please visit the "
       u"<a href='https://bitbucket.org/mandibule/mandibule/issues?status=new&status=open'>Bug Tracker</a>.")


def display():
    """Display the 'About' application dialog box."""
    content = TEMPLATE.format(subtitle=SUBTITLE, p1=P1, p2=P2, p3=P3, p4=P4)
    QtGui.QMessageBox.about(UI['main_window'], TITLE, content)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
