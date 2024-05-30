#! -*- coding: utf8 -*-
from setuptools import setup, find_packages

version = '1.14.dev0'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='collective.dms.basecontent',
    version=version,
    description="Base content types for document management system",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 6.0",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='document management system dms viewer',
    author='Ecreall, Entrouvert, IMIO',
    author_email='cedricmessiant@ecreall.com',
    url='https://github.com/collective/collective.dms.basecontent',
    download_url='https://pypi.org/project/collective.dms.basecontent',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective', 'collective.dms'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.documentviewer',
        'collective.externaleditor',
        'dexterity.localrolesfield',
        'future',
        'imio.helpers>=0.42',
        'plone.api',
        'plone.app.dexterity',
        'plone.directives.form',
        'plone.namedfile',
        'z3c.blobfile',
        'plone.app.contenttypes',
        'plone.app.relationfield',
        'plone.formwidget.contenttree',
        'plone.principalsource',
        'collective.z3cform.select2',
        'z3c.table>=2.2',
    ],
    extras_require={
        'test': ['plone.app.testing',
                 'ecreall.helpers.testing',
                 'plone.app.vocabularies'
                 ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
