# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.0.1.dev0'

setup(name='lk-temp2.base',
      version=version,
      description="",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Bundesamt für Strahlenschutz',
      author_email='mlechner@bfs.de',
      url='http://www.bfs.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'configparser',
          'setuptools',
          'SQLAlchemy',
          'RPi.GPIO'
      ],
      ##code-section entrypoints      
      entry_points="""
      # -*- Entry points: -*-
      """,
      ##/code-section entrypoints
      )
