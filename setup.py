#!/usr/bin/python3

import setuptools
import codecs

setuptools.setup(
    # do not zip the egg file to be able to access the *.xml.gz files
    # within the egg directory easily:
    zip_safe=False,
    name='langtable',
    version='0.0.67',
    packages=setuptools.find_packages(),
    description='guess reasonable defaults for locale, keyboard, territory, ...',
    long_description=codecs.open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    license="GPL-3.0-or-later",
    author='Mike FABIAN',
    author_email='mfabian@redhat.com',
    url='https://github.com/mike-fabian/langtable',
    py_modules=['langtable'],
    package_data={
        'langtable': ['data/*.xml.gz', 'schemas/*.rng'],
    },
    # data_files is for installing the data files outside of the package with:
    #
    #     ./setup.py install_data --install-dir=dirname
    #
    #    data_files = [
    #        ('data',
    #         ['langtable/data/keyboards.xml.gz',
    #          'langtable/data/languages.xml.gz',
    #          'langtable/data/territories.xml.gz',
    #          'langtable/data/timezones.xml.gz',
    #          'langtable/data/timezoneidparts.xml.gz']),
    #        ('schemas',
    #         ['langtable/schemas/keyboards.rng',
    #          'langtable/schemas/languages.rng',
    #          'langtable/schemas/territories.rng',
    #          'langtable/schemas/timezones.rng',
    #          'langtable/schemas/timezoneidparts.rng'])],
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
