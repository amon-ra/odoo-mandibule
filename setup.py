#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import glob
from subprocess import call
from DistUtilsExtra.command import build_i18n
from DistUtilsExtra.auto import setup

name = 'Mandibule'
version = '0.2.0'
description = "Mandibule is a graphical tool to explore OpenERP servers."
keywords = "openerp client developper analyse data metadata model oerplib"
author = u"Sebastien Alix"
author_email = 'seb@usr-src.org'
url = 'https://bitbucket.org/mandibule/mandibule'
download_url = 'https://bitbucket.org/mandibule/mandibule/downloads/Mandibule-%s.tar.gz' % version
license = 'GPLv3'


class BuildPotFiles(build_i18n.build_i18n):
    """Custom 'build_i18n' command to automatically generate the
    POTFILES.in file, and remove it when the work is done.
    """
    def run(self):
        files = [os.path.join(dp, f)
                 for dp, dn, filenames in os.walk('mandibule/')
                 for f in filenames if os.path.splitext(f)[1] == '.py']
        with open('po/POTFILES.in', 'w') as potfiles:
            for file_ in files:
                potfiles.write("%s\n" % file_)
        build_i18n.build_i18n.run(self)
        os.remove('po/POTFILES.in')


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
        'mandibule.addons',
        'mandibule.addons.base',
        'mandibule.addons.base.ui',
        'mandibule.addons.base.actions',
        'mandibule.addons.base.controllers',
        'mandibule.addons.base.forms',
        'mandibule.addons.base.tree',
        'mandibule.addons.dependency',
        'mandibule.addons.relation',
        'mandibule.reg',
        'mandibule.utils',
        'mandibule.widgets',
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
    cmdclass={
        'build_i18n': BuildPotFiles,
    },
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
