#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from distutils.core import setup

name = 'Mandibule'
version = '0.1'
description = "Mandibule is a graphical tool to explore OpenERP servers."
keywords = "openerp client developper analyse data metadata model oerplib"
author = u"Sebastien Alix"
author_email = 'seb@usr-src.org'
#url = 'https://bitbucket.org/Mandibule/'
#download_url = 'https://bitbucket.org/Mandibule/Mandibule-%s.tar.gz' % version
license = 'GPLv3'
doc_build_dir = 'doc/build'
doc_source_dir = 'doc/source'

cmdclass = {}
command_options = {}
# 'build_doc' option
try:
    from sphinx.setup_command import BuildDoc
    if not os.path.exists(doc_build_dir):
        os.mkdir(doc_build_dir)
    cmdclass['build_doc'] = BuildDoc
    command_options['build_doc'] = {
        #'project': ('setup.py', name),
        'version': ('setup.py', version),
        'release': ('setup.py', version),
        'source_dir': ('setup.py', doc_source_dir),
        'build_dir': ('setup.py', doc_build_dir),
        'builder': ('setup.py', 'html'),
    }
except Exception:
    print("No Sphinx module found. You have to install Sphinx "
          "to be able to generate the documentation.")

setup(
    name=name,
    version=version,
    description=description,
    long_description=open('README').read(),
    keywords=keywords,
    author=author,
    author_email=author_email,
    #url=url,
    #download_url=download_url,
    packages=[
        'mandibule',
        'mandibule.controllers',
        'mandibule.utils',
        'mandibule.views',
        'mandibule.views.maintree',
        'mandibule.views.widgets',
        'mandibule.views.workarea',
    ],
    include_package_data=True,
    install_requires=[
        'OERPLib',
        'PySide',
    ],
    scripts=['bin/mandibule'],
    license=license,
    cmdclass=cmdclass,
    command_options=command_options,
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
