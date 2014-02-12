#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import glob
from distutils.core import setup

name = 'Mandibule'
version = '0.2.0'
description = "Mandibule is a graphical tool to explore OpenERP servers."
keywords = "openerp client developper analyse data metadata model oerplib"
author = u"Sebastien Alix"
author_email = 'seb@usr-src.org'
url = 'https://bitbucket.org/mandibule/mandibule'
download_url = 'https://bitbucket.org/mandibule/mandibule/downloads/Mandibule-%s.tar.gz' % version
license = 'GPLv3'

setup(
    name=name,
    version=version,
    description=description,
    long_description=open('README').read(),
    keywords=keywords,
    author=author,
    author_email=author_email,
    url=url,
    download_url=download_url,
    packages=[
        'mandibule',
        'mandibule.controllers',
        'mandibule.utils',
        'mandibule.views',
        'mandibule.views.forms',
        'mandibule.views.maintree',
        'mandibule.views.widgets',
        'mandibule.views.workarea',
    ],
    requires=[
        'OERPLib (>=0.8)',
        'PySide (>=1.1)',
        'pyxdg (>=0.19)',
    ],
    scripts=['bin/mandibule'],
    data_files=[
        ('share/applications', glob.glob('share/applications/*.desktop')),
    ],
    license=license,
    classifiers=[
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Topic :: Office/Business",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Database :: Front-Ends",
    ],
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
