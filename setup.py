#! -*- coding: utf8 -*-
from setuptools import setup, find_packages

version = '0.1'

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

setup(name='collective.dms.basecontent',
      version=version,
      description="Base content types for document management system",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Cédric Messiant',
      author_email='cedricmessiant@ecreall.com',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective', 'collective.dms'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'five.grok',
          'plone.app.dexterity',
          'plone.namedfile',
          'z3c.blobfile',
          'plone.app.relationfield',
          'plone.formwidget.contenttree',
          'collective.dms.thesaurus',
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
