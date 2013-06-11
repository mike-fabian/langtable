#!/usr/bin/env python

from distutils.core import setup


setup(name='langtable',
      version='0.0.5',
      description='guess reasonable defaults for locale, keyboard, territory, ...',
      long_description=open('README').read(),
      license="GPLv3+",
      author='Mike FABIAN',
      author_email='mfabian@redhat.com',
      url='https://github.com/mike-fabian/langtable',
      py_modules=['langtable'],
      data_files = [('', ['data/keyboards.xml', 'data/languages.xml', 'data/territories.xml']),
                    ('schemas', ['schemas/keyboards.rng', 'schemas/languages.rng', 'schemas/territories.rng'])],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup',
      ],
     )
