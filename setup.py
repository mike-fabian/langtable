#!/usr/bin/python3
'''Setup script for langtable.'''
import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='UTF-8') as readme:
    long_description = readme.read()

setuptools.setup(
    # do not zip the egg file to be able to access the *.xml.gz files
    # within the egg directory easily:
    zip_safe=False,
    name='langtable',
    version='0.0.70',
    python_requires='>=3.8',
    packages=setuptools.find_packages(),
    description='guess reasonable defaults for locale, keyboard, territory, ...',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPL-3.0-or-later",
    author='Mike FABIAN',
    author_email='mfabian@redhat.com',
    url='https://github.com/mike-fabian/langtable',
    py_modules=['langtable'],
    package_data={
        'langtable': ['data/*.xml.gz', 'schemas/*.rng'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup',
    ],
)
