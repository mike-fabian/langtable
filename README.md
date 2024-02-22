# langtable

[![PyPI version](https://badge.fury.io/py/langtable.svg)](https://badge.fury.io/py/langtable)

Guessing reasonable defaults for locale, keyboard layout, territory, and language.

## Purpose of this package
_langtable_ is used to guess reasonable defaults for locale, keyboard, territory, …, if part of that information is already known. For example, guess the territory and the keyboard layout if the language is known or guess the language and keyboard layout if the territory is already known.

## License

GPLv3+, see the included file “COPYING”.

Translations for languages and territory names are from CLDR which is governed by the Unicode Terms of Use, see the included file “unicode-license.txt”. The short name for this Unicode license is “MIT”. See:

https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29

## Installation

To install langtable, run

```
     make install DESTDIR=/usr
```

To create a distribution tarball run
```
     make dist
```
To run the test cases in the source directory:
```
     make check
```

## How to use it

```
import langtable
```

Functions in the public API:

```
     parse_locale()
     list_locales()
     list_keyboards()
     list_common_languages()
     list_common_locales()
     list_common_keyboards()
     list_consolefonts()
     list_inputmethods()
     list_timezones()
     list_scripts()
     language_name()
     territory_name()
     timezone_name()
     languageId()
     territoryId()
     supports_ascii()
     list_all_languages()
     list_all_locales()
     list_all_keyboards()
     list_all_territories()
     list_all_timezones()
     list_all_scripts()
     list_all_input_methods()
     list_all_console_fonts()
```

Some examples to show the usage are found in the documentation of the public functions in `langtable.py`.

Some more examples are in the test cases in the file `test_cases.py`.
