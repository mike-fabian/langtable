.. langtable documentation master file, created by
   sphinx-quickstart on Wed Oct 22 12:00:27 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to langtable’s documentation!
*************************************

.. toctree::
   :maxdepth: 2

Purpose of this package
=======================

langtable is used to guess reasonable defaults for locale, keyboard,
territory, …, if part of that information is already known. For
example, guess the territory and the keyboard layout if the language
is known or guess the language and keyboard layout if the territory is
already known.

License
=======

GPLv3+, see the included file “COPYING”.

Translations for languages and territory names are from CLDR which is
governed by the Unicode Terms of Use, see the included file
“unicode-license.txt”. The short name for this Unicode license is
“MIT”. See:

https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29

Installation
============

To install langtable, run

     make install DESTDIR=/usr

To create a distribution tarball run

     make dist

To run the test cases in the source directory:

     make test-local

To run the test cases using the installed files:

     make install DESTDIR=/usr
     make test DESTDIR=/usr

How to use it
=============

import langtable

Functions in the public API
===========================

.. automodule:: langtable
   :members: list_locales, list_keyboards, list_consolefonts, list_inputmethods, list_timezones, language_name, territory_name, languageId, territoryId, supports_ascii

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

