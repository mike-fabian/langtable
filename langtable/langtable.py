# Copyright (c) 2013 Mike FABIAN <mfabian@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''
Guessing reasonable defaults for locale, keyboard layout, territory, and language.

langtable is used to guess reasonable defaults for locale, keyboard,
territory, …, if part of that information is already known. For example,
guess the territory and the keyboard layout if the language is known or guess
the language and keyboard layout if the territory is already known.

Public API:

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

These are the functions which do not start with an “_” in their name.
All global functions and global variables whose name starts with an
“_” are internal and should not be used by a user of langtable.py.

Many of the above public functions have named parameters like

   languageId
   scriptId
   territoryId

and

   languageIdQuery
   scriptIdQuery
   territoryIdQuery

languageId and languageIdQuery may contain a full locale name,
specifying the script and the territory as well.

For example:

    language_name(languageId="sr_Latn_RS")

behaves the same as

    language_name(languageId="sr", scriptId="Latn", territoryId="RS")

If languageId contains a script or a territory, the values found there
are preferred over those given as extra parameters. For example:

    language_name(languageId="sr_Latn_RS", scriptId="Cyrl", territoryId="ME")

behaves the same as

    language_name(languageId="sr", scriptId="Latn", territoryId="RS")

scriptId="Cyrl" and territoryId="ME" are overridden by the values found
in languageId.

It is also possible to put a full locale name in the spelling used by glibc
into languageId. For example:

    language_name(languageId="sr_RS.utf8@latin")

or

    language_name(languageId="sr_RS.UTF-8@latin")

also behave the same as:

    language_name(languageId="sr_Latn_RS")

which is the same as:

    language_name(languageId="sr", scriptId="Latn", territoryId="RS")

langtable always parses languageId, cuts out the encoding and translates
script names in glibc spelling like "latin" to the official
ISO 15924 script codes, see: https://en.wikipedia.org/wiki/ISO_15924
'''

# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name
from typing import List
from typing import Dict
import os
import re
import logging
import gzip
import collections

import xml.parsers.expat
from xml.sax.handler import ContentHandler

Locale = collections.namedtuple(
    'Locale',
    ['language', 'script', 'territory', 'variant', 'encoding'])

_INFO: Dict[str, List[str]] = {'data_files_read': []}

# will be replaced by “make install”:
_DATADIR = '/usr/share/langtable'

# Rank threshold to qualify a
# keyboard layout as prevalent
_KEYBOARD_LAYOUT_RANK_THRESHOLD = 500

# Rank threshold to qualify a
# locale as prevalent
_LOCALE_RANK_THRESHOLD = 500

# For the ICU/CLDR locale pattern see: http://userguide.icu-project.org/locale
# (We ignore the variant code here)
_cldr_locale_pattern = re.compile(
    # language must be 2 or 3 lower case letters:
    '^(?P<language>[a-z]{2,3}'
    # language is only valid if
    +'(?=$|@' # locale string ends here or only options follow
    +'|_[A-Z][a-z]{3}(?=$|@|_[A-Z0-9]{2,3}(?=$|@))' # valid script follows
    +'|_[A-Z0-9]{2,3}(?=$|@)' # valid territory follows
    +'))'
    # script must be 1 upper case letter followed by
    # 3 lower case letters:
    +'(?:_(?P<script>[A-Z][a-z]{3})'
    # script is only valid if
    +'(?=$|@' # locale string ends here or only options follow
    +'|_[A-Z0-9]{2,3}(?=$|@)' # valid territory follows
    +')){0,1}'
    # territory must be 2 upper case letters or 3 digits:
    +'(?:_(?P<territory>[A-Z0-9]{2,3})'
    # territory is only valid if
    +'(?=$|@' # locale string ends here or only options follow
    +')){0,1}')

# http://www.unicode.org/iso15924/iso15924-codes.html
_glibc_script_ids = {
    'latin': 'Latn',
    'iqtelif': 'Latn', # Tatar, tt_RU.UTF-8@iqtelif, http://en.wikipedia.org/wiki/User:Ultranet/%C4%B0QTElif
    'cyrillic': 'Cyrl',
    'devanagari': 'Deva',
}

_territories_db = {}
_languages_db = {}
_keyboards_db = {}
_timezones_db = {}
_timezoneIdParts_db = {}

class territory_db_item: # pylint: disable=too-few-public-methods
    '''Holds information for one territory'''
    def __init__(self, names = None, scripts=None, locales=None, languages=None, keyboards=None, inputmethods=None, consolefonts=None, timezones=None):
        self.names = names
        self.scripts = scripts
        self.locales = locales
        self.languages = languages
        self.keyboards = keyboards
        self.inputmethods = inputmethods
        self.consolefonts = consolefonts
        self.timezones = timezones

class language_db_item: # pylint: disable=too-few-public-methods
    '''Holds information for one language'''
    def __init__(self, iso639_1=None, iso639_2_t=None, iso639_2_b=None, names=None, scripts=None, locales=None, territories=None, keyboards=None, inputmethods=None, consolefonts=None, timezones=None):
        self.iso639_1 = iso639_1
        self.iso639_2_t = iso639_2_t
        self.iso639_2_b = iso639_2_b
        self.names = names
        self.scripts = scripts
        self.locales = locales
        self.territories = territories
        self.keyboards = keyboards
        self.inputmethods = inputmethods
        self.consolefonts = consolefonts
        self.timezones = timezones

class keyboard_db_item: # pylint: disable=too-few-public-methods
    '''Holds information for one keyboard layout'''
    def __init__(self, description=None, ascii=True, languages=None, territories = None, comment=None):
        self.description = description
        self.ascii  = ascii
        self.comment = comment
        self.languages = languages
        self.territories = territories

class timezone_db_item: # pylint: disable=too-few-public-methods
    '''Holds information for one timezone'''
    def __init__(self, names=None):
        self.names = names

class timezoneIdPart_db_item: # pylint: disable=too-few-public-methods
    '''Holds information for one timezone part'''
    def __init__(self, names=None):
        self.names = names

# xml.sax.handler.ContentHandler is not inherited from the 'object' class,
# 'super' keyword wouldn't work, we need to inherit it on our own
class LangtableContentHandler(ContentHandler):
    """
    A base class inherited from the xml.sax.handler.ContentHandler class
    providing handling for SAX events produced when parsing the langtable data
    files.

    """

    def __init__(self):
        super().__init__()
        # internal attribute used to set where the upcoming text data should be
        # stored
        self._save_to = None

    def characters(self, content):
        """Handler for the text data event."""

        if self._save_to is None:
            # don't know where to save data
            return

        # text content may split in multiple events
        old_value = getattr(self, self._save_to)
        if old_value:
            new_value = old_value + content
        else:
            new_value = content

        setattr(self, self._save_to, new_value)

class TerritoriesContentHandler(LangtableContentHandler):
    """Handler for SAX events produced when parsing the territories.xml file."""

    def __init__(self):
        super().__init__()

        # simple values
        self._territoryId = None

        # helper variables
        self._item_id = None
        self._item_rank = None
        self._item_name = None

        # dictionaries
        self._names = None
        self._scripts = None
        self._locales = None
        self._languages = None
        self._keyboards = None
        self._inputmethods = None
        self._consolefonts = None
        self._timezones = None

    def startElement(self, name, attrs):
        if name == "territory":
            self._names = {}
            self._scripts = {}
            self._locales = {}
            self._languages = {}
            self._keyboards = {}
            self._inputmethods = {}
            self._consolefonts = {}
            self._timezones = {}

        # non-dict values
        elif name == "territoryId":
            self._save_to = "_territoryId"

        # dict items
        elif name in ("languageId", "scriptId", "localeId", "keyboardId", "inputmethodId",
                      "consolefontId", "timezoneId"):
            self._save_to = "_item_id"
        elif name == "trName":
            self._save_to = "_item_name"
        elif name == "rank":
            self._save_to = "_item_rank"

    def endElement(self, name):
        # we don't allow text to appear on the same level as elements so outside
        # of an element no text should appear
        self._save_to = None

        if name == "territory":
            _territories_db[str(self._territoryId)] = territory_db_item(
                names = self._names,
                scripts = self._scripts,
                locales = self._locales,
                languages = self._languages,
                keyboards = self._keyboards,
                inputmethods = self._inputmethods,
                consolefonts = self._consolefonts,
                timezones = self._timezones)

            # clean after ourselves
            self._territoryId = None
            self._names = None
            self._scripts = None
            self._locales = None
            self._languages = None
            self._keyboards = None
            self._inputmethods = None
            self._consolefonts = None
            self._timezones = None

        # populating dictionaries
        elif name == "name":
            self._names[str(self._item_id)] = self._item_name
            self._clear_item()
        elif name == "script":
            self._scripts[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "locale":
            self._locales[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "language":
            self._languages[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "keyboard":
            self._keyboards[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "inputmethod":
            self._inputmethods[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "consolefont":
            self._consolefonts[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "timezone":
            self._timezones[str(self._item_id)] = int(self._item_rank)
            self._clear_item()

    def _clear_item(self):
        self._item_id = None
        self._item_name = None
        self._item_rank = None

class KeyboardsContentHandler(LangtableContentHandler):
    """Handler for SAX events produced when parsing the keyboards.xml file."""

    def __init__(self):
        super().__init__()

        # simple values
        self._keyboardId = None
        self._description = None
        self._ascii = None
        self._comment = None

        # helper variables
        self._item_id = None
        self._item_rank = None

        # dictionaries
        self._languages = None
        self._territories = None

    def startElement(self, name, attrs):
        if name == "keyboard":
            self._languages = {}
            self._territories = {}

        # non-dict values
        elif name == "keyboardId":
            self._save_to = "_keyboardId"
        elif name == "description":
            self._save_to = "_description"
        elif name == "ascii":
            self._save_to = "_ascii"
        elif name == "comment":
            self._save_to = "_comment"

        # dict items
        elif name in ("languageId", "territoryId"):
            self._save_to = "_item_id"
        elif name == "rank":
            self._save_to = "_item_rank"

    def endElement(self, name):
        # we don't allow text to appear on the same level as elements so outside
        # of an element no text should appear
        self._save_to = None

        if name == "keyboard":
            _keyboards_db[str(self._keyboardId)] = keyboard_db_item(
                description = self._description,
                ascii = self._ascii == "True",
                comment = self._comment,
                languages = self._languages,
                territories = self._territories)

            # clean after ourselves
            self._keyboardId = None
            self._description = None
            self._ascii = None
            self._comment = None
            self._languages = None
            self._territories = None

        # populating dictionaries
        elif name == "language":
            self._languages[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "territory":
            self._territories[str(self._item_id)] = int(self._item_rank)
            self._clear_item()

    def _clear_item(self):
        self._item_id = None
        self._item_rank = None

class LanguagesContentHandler(LangtableContentHandler):
    """Handler for SAX events produced when parsing the languages.xml file."""

    def __init__(self):
        super().__init__()
        # simple values
        self._languageId = None
        self._iso639_1 = None
        self._iso639_2_t = None
        self._iso639_2_b = None

        # helper variables
        self._item_id = None
        self._item_rank = None
        self._item_name = None

        # flag to distinguish 'languageId' elements inside and outside of the
        # 'names' element
        self._in_names = False

        # dictionaries
        self._names = None
        self._scripts = None
        self._locales = None
        self._territories = None
        self._keyboards = None
        self._inputmethods = None
        self._consolefonts = None
        self._timezones = None

    def startElement(self, name, attrs):
        if name == "language":
            self._names = {}
            self._scripts = {}
            self._locales = {}
            self._territories = {}
            self._keyboards = {}
            self._inputmethods = {}
            self._consolefonts = {}
            self._timezones = {}

        # non-dict values
        elif name == "languageId" and not self._in_names:
            # ID of the language
            self._save_to = "_languageId"
        elif name == "iso639-1":
            self._save_to = "_iso639_1"
        elif name == "iso639-2-t":
            self._save_to = "_iso639_2_t"
        elif name == "iso639-2-b":
            self._save_to = "_iso639_2_b"
        elif name == "names":
            self._in_names = True

        # dict items
        elif name in ("scriptId", "localeId", "territoryId", "keyboardId", "inputmethodId",
                      "consolefontId", "timezoneId"):
            self._save_to = "_item_id"
        elif name == "languageId" and self._in_names:
            # ID of the translated name's language
            self._save_to = "_item_id"
        elif name == "trName":
            self._save_to = "_item_name"
        elif name == "rank":
            self._save_to = "_item_rank"

    def endElement(self, name):
        # we don't allow text to appear on the same level as elements so outside
        # of an element no text should appear
        self._save_to = None

        if name == "language":
            _languages_db[str(self._languageId)] = language_db_item(
                iso639_1 = self._iso639_1,
                iso639_2_t = self._iso639_2_t,
                iso639_2_b = self._iso639_2_b,
                names = self._names,
                scripts = self._scripts,
                locales = self._locales,
                territories = self._territories,
                keyboards = self._keyboards,
                inputmethods = self._inputmethods,
                consolefonts = self._consolefonts,
                timezones = self._timezones)

            # clean after ourselves
            self._languageId = None
            self._iso639_1 = None
            self._iso639_2_t = None
            self._iso639_2_b = None
            self._names = None
            self._scripts = None
            self._locales = None
            self._territories = None
            self._keyboards = None
            self._inputmethods = None
            self._consolefonts = None
            self._timezones = None

        # leaving the "names" element
        elif name == "names":
            self._in_names = False

        # populating dictionaries
        elif name == "name":
            self._names[str(self._item_id)] = self._item_name
            self._clear_item()
        elif name == "script":
            self._scripts[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "locale":
            self._locales[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "territory":
            self._territories[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "keyboard":
            self._keyboards[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "inputmethod":
            self._inputmethods[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "consolefont":
            self._consolefonts[str(self._item_id)] = int(self._item_rank)
            self._clear_item()
        elif name == "timezone":
            self._timezones[str(self._item_id)] = int(self._item_rank)
            self._clear_item()

    def _clear_item(self):
        self._item_id = None
        self._item_name = None
        self._item_rank = None

class TimezonesContentHandler(LangtableContentHandler):
    """Handler for SAX events produced when parsing the timezones.xml file."""

    def __init__(self):
        super().__init__()
        # simple values
        self._timezoneId = None

        # helper variables
        self._item_id = None
        self._item_name = None

        # dictionaries
        self._names = None

    def startElement(self, name, attrs):
        if name == "timezone":
            self._names = {}

        # non-dict values
        elif name == "timezoneId":
            # ID of the timezone
            self._save_to = "_timezoneId"

        # dict items
        elif name == "languageId":
            # ID of the translated timezone's language
            self._save_to = "_item_id"
        elif name == "trName":
            self._save_to = "_item_name"

    def endElement(self, name):
        # we don't allow text to appear on the same level as elements so outside
        # of an element no text should appear
        self._save_to = None

        if name == "timezone":
            _timezones_db[str(self._timezoneId)] = timezone_db_item(
                names = self._names)

            # clean after ourselves
            self._timezoneId = None
            self._names = None

        # populating dictionaries
        elif name == "name":
            self._names[str(self._item_id)] = self._item_name
            self._clear_item()

    def _clear_item(self):
        self._item_id = None
        self._item_name = None

class TimezoneIdPartsContentHandler(LangtableContentHandler):
    """Handler for SAX events produced when parsing the timezoneidparts.xml file."""

    def __init__(self):
        super().__init__()
        # simple values
        self._timezoneIdPartId = None

        # helper variables
        self._item_id = None
        self._item_name = None

        # dictionaries
        self._names = None

    def startElement(self, name, attrs):
        if name == "timezoneIdPart":
            self._names = {}

        # non-dict values
        elif name == "timezoneIdPartId":
            # partial timezone ID
            self._save_to = "_timezoneIdPartId"

        # dict items
        elif name == "languageId":
            # ID of the translated partial timezone ID's language
            self._save_to = "_item_id"
        elif name == "trName":
            self._save_to = "_item_name"

    def endElement(self, name):
        # we don't allow text to appear on the same level as elements so outside
        # of an element no text should appear
        self._save_to = None

        if name == "timezoneIdPart":
            _timezoneIdParts_db[str(self._timezoneIdPartId)] = timezoneIdPart_db_item(
                names = self._names)

            # clean after ourselves
            self._timezoneIdPartId = None
            self._names = None

        # populating dictionaries
        elif name == "name":
            self._names[str(self._item_id)] = self._item_name
            self._clear_item()

    def _clear_item(self):
        self._item_id = None
        self._item_name = None

def _write_territories_file(file):
    '''
    Only for internal use
    '''
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<territories>\n')
    for territoryId in sorted(_territories_db):
        file.write('  <territory>\n')
        file.write('    <territoryId>'+territoryId+'</territoryId>\n')
        names = _territories_db[territoryId].names
        file.write('    <names>\n')
        for name in sorted(names):
            file.write(
                '      <name>'
                +'<languageId>'+name+'</languageId>'
                +'<trName>'+names[name].replace('&', '&amp;')+'</trName>'
                +'</name>\n')
        file.write('    </names>\n')
        scripts = _territories_db[territoryId].scripts
        file.write('    <scripts>\n')
        for scriptId, rank in sorted(scripts.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <script>'
                +'<scriptId>'+scriptId+'</scriptId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</script>\n')
        file.write('    </scripts>\n')
        locales = _territories_db[territoryId].locales
        file.write('    <locales>\n')
        for localeId, rank in sorted(locales.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <locale>'
                +'<localeId>'+localeId+'</localeId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</locale>\n')
        file.write('    </locales>\n')
        languages = _territories_db[territoryId].languages
        file.write('    <languages>\n')
        for languageId, rank in sorted(languages.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <language>'
                +'<languageId>'+languageId+'</languageId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</language>\n')
        file.write('    </languages>\n')
        keyboards = _territories_db[territoryId].keyboards
        file.write('    <keyboards>\n')
        for keyboardId, rank in sorted(keyboards.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <keyboard>'
                +'<keyboardId>'+keyboardId+'</keyboardId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</keyboard>\n')
        file.write('    </keyboards>\n')
        inputmethods = _territories_db[territoryId].inputmethods
        file.write('    <inputmethods>\n')
        for inputmethodId, rank in sorted(inputmethods.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <inputmethod>'
                +'<inputmethodId>'+inputmethodId+'</inputmethodId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</inputmethod>\n')
        file.write('    </inputmethods>\n')
        consolefonts = _territories_db[territoryId].consolefonts
        file.write('    <consolefonts>\n')
        for consolefontId, rank in sorted(consolefonts.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <consolefont>'
                +'<consolefontId>'+consolefontId+'</consolefontId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</consolefont>\n')
        file.write('    </consolefonts>\n')
        timezones = _territories_db[territoryId].timezones
        file.write('    <timezones>\n')
        for timezoneId, rank in sorted(timezones.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <timezone>'
                +'<timezoneId>'+timezoneId+'</timezoneId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</timezone>\n')
        file.write('    </timezones>\n')
        file.write('  </territory>\n')
    file.write('</territories>\n')

def _write_languages_file(file):
    '''
    Only for internal use
    '''
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<languages>\n')
    for languageId in sorted(_languages_db):
        file.write('  <language>\n')
        file.write('    <languageId>'+languageId+'</languageId>\n')
        file.write('    <iso639-1>'+str(_languages_db[languageId].iso639_1)+'</iso639-1>\n')
        file.write('    <iso639-2-t>'+str(_languages_db[languageId].iso639_2_t)+'</iso639-2-t>\n')
        file.write('    <iso639-2-b>'+str(_languages_db[languageId].iso639_2_b)+'</iso639-2-b>\n')
        names = _languages_db[languageId].names
        file.write('    <names>\n')
        for name in sorted(names):
            file.write(
                '      <name>'
                +'<languageId>'+name+'</languageId>'
                +'<trName>'+names[name]+'</trName>'
                +'</name>\n')
        file.write('    </names>\n')
        scripts = _languages_db[languageId].scripts
        file.write('    <scripts>\n')
        for scriptId, rank in sorted(scripts.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <script>'
                +'<scriptId>'+scriptId+'</scriptId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</script>\n')
        file.write('    </scripts>\n')
        locales = _languages_db[languageId].locales
        file.write('    <locales>\n')
        for localeId, rank in sorted(locales.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <locale>'
                +'<localeId>'+localeId+'</localeId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</locale>\n')
        file.write('    </locales>\n')
        territories = _languages_db[languageId].territories
        file.write('    <territories>\n')
        for territoryId, rank in sorted(territories.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <territory>'
                +'<territoryId>'+territoryId+'</territoryId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</territory>\n')
        file.write('    </territories>\n')
        keyboards = _languages_db[languageId].keyboards
        file.write('    <keyboards>\n')
        for keyboardId, rank in sorted(keyboards.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <keyboard>'
                +'<keyboardId>'+keyboardId+'</keyboardId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</keyboard>\n')
        file.write('    </keyboards>\n')
        inputmethods = _languages_db[languageId].inputmethods
        file.write('    <inputmethods>\n')
        for inputmethodId, rank in sorted(inputmethods.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <inputmethod>'
                +'<inputmethodId>'+inputmethodId+'</inputmethodId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</inputmethod>\n')
        file.write('    </inputmethods>\n')
        consolefonts = _languages_db[languageId].consolefonts
        file.write('    <consolefonts>\n')
        for consolefontId, rank in sorted(consolefonts.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <consolefont>'
                +'<consolefontId>'+consolefontId+'</consolefontId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</consolefont>\n')
        file.write('    </consolefonts>\n')
        timezones = _languages_db[languageId].timezones
        file.write('    <timezones>\n')
        for timezoneId, rank in sorted(timezones.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <timezone>'
                +'<timezoneId>'+timezoneId+'</timezoneId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</timezone>\n')
        file.write('    </timezones>\n')
        file.write('  </language>\n')
    file.write('</languages>\n')

def _write_keyboards_file(file):
    '''
    Only for internal use
    '''
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<keyboards>\n')
    for keyboardId in sorted(_keyboards_db):
        file.write('  <keyboard>\n')
        file.write('    <keyboardId>'+keyboardId+'</keyboardId>\n')
        file.write('    <description>'+_keyboards_db[keyboardId].description+'</description>\n')
        file.write('    <ascii>'+str(_keyboards_db[keyboardId].ascii)+'</ascii>\n')
        if _keyboards_db[keyboardId].comment is not None:
            file.write('    <comment>'+_keyboards_db[keyboardId].comment+'</comment>\n')
        languages = _keyboards_db[keyboardId].languages
        file.write('    <languages>\n')
        for languageId, rank in sorted(languages.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <language>'
                +'<languageId>'+languageId+'</languageId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</language>\n')
        file.write('    </languages>\n')
        territories = _keyboards_db[keyboardId].territories
        file.write('    <territories>\n')
        for territoryId, rank in sorted(territories.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <territory>'
                +'<territoryId>'+territoryId+'</territoryId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</territory>\n')
        file.write('    </territories>\n')
        file.write('  </keyboard>\n')
    file.write('</keyboards>\n')

def _write_timezones_file(file):
    '''
    Only for internal use
    '''
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<timezones>\n')
    for timezoneId in sorted(_timezones_db):
        file.write('  <timezone>\n')
        file.write('    <timezoneId>'+timezoneId+'</timezoneId>\n')
        names = _timezones_db[timezoneId].names
        file.write('    <names>\n')
        for name in sorted(names):
            file.write(
                '      <name>'
                +'<languageId>'+name+'</languageId>'
                +'<trName>'+names[name]+'</trName>'
                +'</name>\n')
        file.write('    </names>\n')
        file.write('  </timezone>\n')
    file.write('</timezones>\n')

def _write_timezoneIdParts_file(file):
    '''
    Only for internal use
    '''
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<timezoneIdParts>\n')
    for timezoneIdPartId in sorted(_timezoneIdParts_db):
        file.write('  <timezoneIdPart>\n')
        file.write('    <timezoneIdPartId>'+timezoneIdPartId+'</timezoneIdPartId>\n')
        names = _timezoneIdParts_db[timezoneIdPartId].names
        file.write('    <names>\n')
        for name in sorted(names):
            file.write(
                '      <name>'
                +'<languageId>'+name+'</languageId>'
                +'<trName>'+names[name]+'</trName>'
                +'</name>\n')
        file.write('    </names>\n')
        file.write('  </timezoneIdPart>\n')
    file.write('</timezoneIdParts>\n')

def _expat_parse(file, sax_handler):
    """
    Only for internal use. Parses a given file object with a given SAX handler
    using an expat parser.
    """

    parser = xml.parsers.expat.ParserCreate()
    parser.StartElementHandler = sax_handler.startElement
    parser.EndElementHandler = sax_handler.endElement
    parser.CharacterDataHandler = sax_handler.characters
    parser.ParseFile(file)

def _read_file(filename, sax_handler):
    '''
    Only for internal use
    '''
    for directory in (
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
            os.path.join(_DATADIR, 'data')):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            with open(path, mode='rb') as file:
                logging.info('reading file=%s', file)
                _expat_parse(file, sax_handler)
                _INFO['data_files_read'].append(path)
            return
        path = os.path.join(directory, filename+'.gz')
        if os.path.isfile(path):
            with gzip.open(path, mode='rb') as file:
                logging.info('reading file=%s', file)
                _expat_parse(file, sax_handler)
                _INFO['data_files_read'].append(path)
            return
    logging.info('no readable file found.')

def _write_files(territoriesfilename, languagesfilename, keyboardsfilename, timezonesfilename, timezoneidpartsfilename):
    '''
    Only for internal use
    '''
    with open(territoriesfilename, 'w', encoding='UTF-8') as territoriesfile:
        logging.info('writing territories file=%s', territoriesfile)
        _write_territories_file(territoriesfile)
    with open(languagesfilename, 'w', encoding='UTF-8') as languagesfile:
        logging.info('writing languages file=%s', languagesfile)
        _write_languages_file(languagesfile)
    with open(keyboardsfilename, 'w', encoding='UTF-8') as keyboardsfile:
        logging.info('writing keyboards file=%s', keyboardsfile)
        _write_keyboards_file(keyboardsfile)
    with open(keyboardsfilename, 'w', encoding='UTF-8') as keyboardsfile:
        logging.info('writing keyboards file=%s', keyboardsfile)
        _write_keyboards_file(keyboardsfile)
    with open(timezonesfilename, 'w', encoding='UTF-8') as timezonesfile:
        logging.info('writing timezones file=%s', timezonesfile)
        _write_timezones_file(timezonesfile)
    with open(timezoneidpartsfilename, 'w', encoding='UTF-8') as timezoneidpartsfile:
        logging.info('writing timezoneidparts file=%s', timezoneidpartsfile)
        _write_timezoneIdParts_file(timezoneidpartsfile)

def _dictionary_to_ranked_list(dictionary, reverse=True):
    sorted_list = []
    for item in sorted(dictionary, key=lambda x: (dictionary.get(x), x), reverse=reverse):
        if dictionary[item] != 0:
            sorted_list.append([item, dictionary[item]])
    return sorted_list

def _ranked_list_to_list(ranked_list):
    return list(map(lambda x: x[0], ranked_list))

def _make_ranked_list_concise(ranked_list, cut_off_factor=1000):
    if not len(ranked_list) > 1:
        return ranked_list
    for i in range(0,len(ranked_list)-1):
        if ranked_list[i][1]/ranked_list[i+1][1] > cut_off_factor:
            ranked_list = ranked_list[0:i+1]
            break
    return ranked_list

def _capitalize_name(text, languageId='', scriptId='', territoryId='', languageIdQuery='', scriptIdQuery='', territoryIdQuery=''): # pylint: disable=unused-argument
    '''
    Title cases the first letter of “text”

    But make exceptions for certain languages where always upper casing the first
    letter does not make sense even for standalone strings.

    :param text: The text which may need its first letter uppercased to be
                 used standalone
    :type text: string
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :param languageIdQuery: identifier for the language used in the result
    :type languageIdQuery: string
    :param scriptIdQuery: identifier for the script used in the result
    :type scriptIdQuery: string
    :param territoryIdQuery: identifier for the territory used in the result
    :type territoryIdQuery: string
    :rtype: string
    '''
    if not text or text[0].istitle():
        return text
    if not languageIdQuery:
        languageIdQuery = languageId
    if not languageIdQuery:
        languageIdQuery = 'en'
    for lang in ('ka', 'nr', 'ss', 'xh', 'yo', 'zu'):
        if re.match(rf'^{lang}', languageIdQuery):
            return text
    return text[0].capitalize() + text[1:]

def parse_locale(localeId):
    '''
    Parses a locale name in glibc or CLDR format and returns
    language, script, territory, variant, and encoding

    :param localeId: The name of the locale
    :type localeId: string
    :return: The parts of the locale: language, script, territory, variant, encoding
    :rtype: A namedtuple of strings
            Locale(language=string,
                   script=string,
                   territory=string,
                   variant=string,
                   encoding=string)

    It replaces glibc names for scripts like “latin”
    with the iso-15924 script names like “Latn”.
    I.e. these inputs all give the same result:

        “sr_latin_RS”
        “sr_Latn_RS”
        “sr_RS@latin”
        “sr_RS@Latn”

    Examples:

    >>> parse_locale('de_DE')
    Locale(language='de', script='', territory='DE', variant='', encoding='')

    >>> parse_locale('de_DE.UTF-8')
    Locale(language='de', script='', territory='DE', variant='', encoding='UTF-8')

    >>> parse_locale('de_DE.utf8')
    Locale(language='de', script='', territory='DE', variant='', encoding='utf8')

    >>> parse_locale('de_DE@euro')
    Locale(language='de', script='', territory='DE', variant='EURO', encoding='')

    >>> parse_locale('de_DE.ISO-8859-15')
    Locale(language='de', script='', territory='DE', variant='', encoding='ISO-8859-15')

    >>> parse_locale('de_DE.ISO-8859-15@euro')
    Locale(language='de', script='', territory='DE', variant='EURO', encoding='ISO-8859-15')

    >>> parse_locale('de_DE.iso885915@euro')
    Locale(language='de', script='', territory='DE', variant='EURO', encoding='iso885915')

    >>> parse_locale('gez_ER.UTF-8@abegede')
    Locale(language='gez', script='', territory='ER', variant='ABEGEDE', encoding='UTF-8')

    >>> parse_locale('ar_ER.UTF-8@saaho')
    Locale(language='ar', script='', territory='ER', variant='SAAHO', encoding='UTF-8')

    >>> parse_locale('zh_Hant_TW')
    Locale(language='zh', script='Hant', territory='TW', variant='', encoding='')

    >>> parse_locale('zh_TW')
    Locale(language='zh', script='', territory='TW', variant='', encoding='')

    >>> parse_locale('es_419')
    Locale(language='es', script='', territory='419', variant='', encoding='')

    >>> parse_locale('sr_latin_RS')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='')

    >>> parse_locale('sr_Latn_RS')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='')

    >>> parse_locale('sr_RS@latin')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='')

    >>> parse_locale('sr_RS@Latn')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='')

    >>> parse_locale('sr_RS.UTF-8@latin')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='UTF-8')

    >>> parse_locale('ca_ES')
    Locale(language='ca', script='', territory='ES', variant='', encoding='')

    >>> parse_locale('ca_ES.UTF-8')
    Locale(language='ca', script='', territory='ES', variant='', encoding='UTF-8')

    >>> parse_locale('ca_ES_VALENCIA')
    Locale(language='ca', script='', territory='ES', variant='VALENCIA', encoding='')

    >>> parse_locale('ca_Latn_ES_VALENCIA')
    Locale(language='ca', script='Latn', territory='ES', variant='VALENCIA', encoding='')

    >>> parse_locale('ca_ES.UTF-8@valencia')
    Locale(language='ca', script='', territory='ES', variant='VALENCIA', encoding='UTF-8')

    >>> parse_locale('ca_ES@valencia')
    Locale(language='ca', script='', territory='ES', variant='VALENCIA', encoding='')

    >>> parse_locale('en_US_POSIX')
    Locale(language='en', script='', territory='US', variant='POSIX', encoding='')

    >>> parse_locale('POSIX')
    Locale(language='en', script='', territory='US', variant='POSIX', encoding='')

    >>> parse_locale('C')
    Locale(language='en', script='', territory='US', variant='POSIX', encoding='')

    >>> parse_locale('C.UTF-8')
    Locale(language='en', script='', territory='US', variant='POSIX', encoding='UTF-8')
    '''
    language = ''
    script = ''
    territory = ''
    variant = ''
    encoding = ''
    if localeId:
        dot_index = localeId.find('.')
        at_index = localeId.find('@')
        if 0 <= dot_index < at_index:
            encoding  = localeId[dot_index + 1:at_index]
            localeId = localeId[:dot_index] + localeId[at_index:]
        elif dot_index >= 0:
            encoding = localeId[dot_index + 1:]
            localeId = localeId[:dot_index]
    if localeId:
        valencia_index = localeId.lower().find('@valencia')
        if valencia_index < 0:
            valencia_index = localeId.upper().find('_VALENCIA')
        if valencia_index >= 0:
            variant = 'VALENCIA'
            localeId = localeId[:valencia_index]
    if localeId:
        if localeId in ('C', 'POSIX', 'en_US_POSIX'):
            language = 'en'
            territory = 'US'
            variant = 'POSIX'
            localeId = ''
    if localeId:
        for key, script_id_iso in _glibc_script_ids.items():
            localeId = localeId.replace(key, script_id_iso)
            if localeId.endswith('@' + script_id_iso):
                script = script_id_iso
                localeId = localeId.replace('@' + script_id_iso, '')
    if localeId:
        at_index = localeId.find('@')
        if at_index >= 0:
            # If there is still an @ followed by something, it is not
            # a known script, otherwise it would have been parsed as a
            # script in the previous section. In that case it is a
            # variant of the locale.
            variant = localeId[at_index + 1:].upper()
            localeId = localeId[:at_index]
    if localeId:
        match = _cldr_locale_pattern.match(localeId)
        if match:
            language = match.group('language')
            if match.group('script'):
                script = match.group('script')
            if match.group('territory'):
                territory = match.group('territory')
        else:
            logging.info("localeId contains invalid locale id=%s", localeId)
    return Locale(language=language,
                  script=script,
                  territory=territory,
                  variant=variant,
                  encoding=encoding)

def _parse_and_split_languageId(languageId='', scriptId='', territoryId=''):
    '''
    Parses languageId and if it contains a valid ICU locale id,
    returns the values for language, script, and territory found
    in languageId instead of the original values given.

    Before parsing, it replaces glibc names for scripts like “latin”
    with the iso-15924 script names like “Latn”, both in the
    languageId and the scriptId parameter. I.e.  language id like
    “sr_latin_RS” is accepted as well and treated the same as
    “sr_Latn_RS”.

    Examples:

    >>> _parse_and_split_languageId(languageId='de_DE')
    Locale(language='de', script='', territory='DE', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='de_DE.UTF-8')
    Locale(language='de', script='', territory='DE', variant='', encoding='UTF-8')

    >>> _parse_and_split_languageId(languageId='de_DE.utf8')
    Locale(language='de', script='', territory='DE', variant='', encoding='utf8')

    >>> _parse_and_split_languageId(languageId='de_DE@euro')
    Locale(language='de', script='', territory='DE', variant='EURO', encoding='')

    >>> _parse_and_split_languageId(languageId='de_DE.ISO-8859-15')
    Locale(language='de', script='', territory='DE', variant='', encoding='ISO-8859-15')

    >>> _parse_and_split_languageId(languageId='de_DE.ISO-8859-15@euro')
    Locale(language='de', script='', territory='DE', variant='EURO', encoding='ISO-8859-15')

    >>> _parse_and_split_languageId(languageId='de_DE.iso885915@euro')
    Locale(language='de', script='', territory='DE', variant='EURO', encoding='iso885915')

    >>> _parse_and_split_languageId(languageId='gez_ER.UTF-8@abegede')
    Locale(language='gez', script='', territory='ER', variant='ABEGEDE', encoding='UTF-8')

    >>> _parse_and_split_languageId(languageId='ar_ER.UTF-8@saaho')
    Locale(language='ar', script='', territory='ER', variant='SAAHO', encoding='UTF-8')

    >>> _parse_and_split_languageId(languageId='zh_Hant_TW')
    Locale(language='zh', script='Hant', territory='TW', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='zh_TW')
    Locale(language='zh', script='Hant', territory='TW', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='zh_Hans_CN')
    Locale(language='zh', script='Hans', territory='CN', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='zh_CN')
    Locale(language='zh', script='Hans', territory='CN', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='es_419')
    Locale(language='es', script='', territory='419', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='sr_latin_RS')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='sr_Latn_RS')
    Locale(language='sr', script='Latn', territory='RS', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_ES')
    Locale(language='ca', script='', territory='ES', variant='', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_ES.UTF-8')
    Locale(language='ca', script='', territory='ES', variant='', encoding='UTF-8')

    >>> _parse_and_split_languageId(languageId='ca_ES_VALENCIA')
    Locale(language='ca_ES_VALENCIA', script='', territory='ES', variant='VALENCIA', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_Latn_ES_VALENCIA')
    Locale(language='ca_ES_VALENCIA', script='Latn', territory='ES', variant='VALENCIA', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_Latn_ES_valencia')
    Locale(language='ca_ES_VALENCIA', script='Latn', territory='ES', variant='VALENCIA', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_ES.UTF-8@valencia')
    Locale(language='ca_ES_VALENCIA', script='', territory='ES', variant='VALENCIA', encoding='UTF-8')

    >>> _parse_and_split_languageId(languageId='ca_ES@valencia')
    Locale(language='ca_ES_VALENCIA', script='', territory='ES', variant='VALENCIA', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_Latn_ES@valencia')
    Locale(language='ca_ES_VALENCIA', script='Latn', territory='ES', variant='VALENCIA', encoding='')

    >>> _parse_and_split_languageId(languageId='ca_Latn_ES@VALENCIA')
    Locale(language='ca_ES_VALENCIA', script='Latn', territory='ES', variant='VALENCIA', encoding='')
    '''
    locale = parse_locale(languageId)
    if locale.variant == 'POSIX': # ignore the posix variant
        locale = Locale(language=locale.language,
                        script=locale.script,
                        territory=locale.territory,
                        variant='',
                        encoding=locale.encoding)
    if locale.variant == 'VALENCIA':
        locale = Locale(language='ca_ES_VALENCIA',
                        script=locale.script,
                        territory=locale.territory,
                        variant=locale.variant,
                        encoding=locale.encoding)
    if not locale.script and scriptId:
        scriptId = _glibc_script_ids.get(scriptId, scriptId)
        locale = Locale(language=locale.language,
                        script=scriptId,
                        territory=locale.territory,
                        variant=locale.variant,
                        encoding=locale.encoding)
    if not locale.territory and territoryId:
        locale = Locale(language=locale.language,
                        script=locale.script,
                        territory=territoryId,
                        variant=locale.variant,
                        encoding=locale.encoding)
    # if the language is Chinese and only the territory is given
    # but not the script, add the default script for the territory:
    if locale.language in ('zh', 'cmn') and locale.territory and not locale.script:
        if locale.territory in ['CN', 'SG']:
            locale = Locale(language=locale.language,
                            script='Hans',
                            territory=locale.territory,
                            variant=locale.variant,
                            encoding=locale.encoding)
        elif locale.territory in ['HK', 'MO', 'TW']:
            locale = Locale(language=locale.language,
                            script='Hant',
                            territory=locale.territory,
                            variant=locale.variant,
                            encoding=locale.encoding)
    return locale

def territory_name(territoryId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None, fallback=True):
    '''Query translations of territory names

    :param territoryId: identifier for the territory
    :type territoryId: string
    :param languageIdQuery: identifier for the language used in the result
    :type languageIdQuery: string
    :param scriptIdQuery: identifier for the script used in the result
    :type scriptIdQuery: string
    :param territoryIdQuery: identifier for the territory used in the result
    :type territoryIdQuery: string
    :param fallback: Whether a fallback to English should be returned if the
                     name cannot be found in the requested language.
    :type fallback: Boolean
    :rtype: string

    **Examples:**

    Switzerland is called “Schweiz” in German:

    >>> print(territory_name(territoryId="CH", languageIdQuery="de"))
    Schweiz

    And it is called “Svizzera” in Italian:

    >>> print(territory_name(territoryId="CH", languageIdQuery="it"))
    Svizzera

    And it is called “スイス” in Japanese:

    >>> print(territory_name(territoryId="CH", languageIdQuery="ja"))
    スイス
    '''
    return _capitalize_name(
        _territory_name(territoryId=territoryId,
                         languageIdQuery=languageIdQuery,
                         scriptIdQuery=scriptIdQuery,
                         territoryIdQuery=territoryIdQuery,
                         fallback=fallback),
        territoryId=territoryId,
        languageIdQuery=languageIdQuery,
        scriptIdQuery=scriptIdQuery,
        territoryIdQuery=territoryIdQuery)

def _territory_name(territoryId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None, fallback=True):
    '''Internal function to query translations of territory names

    :param territoryId: identifier for the territory
    :type territoryId: string
    :param languageIdQuery: identifier for the language used in the result
    :type languageIdQuery: string
    :param scriptIdQuery: identifier for the script used in the result
    :type scriptIdQuery: string
    :param territoryIdQuery: identifier for the territory used in the result
    :type territoryIdQuery: string
    :param fallback: Whether a fallback to English should be returned if the
                     name cannot be found in the requested language.
    :type fallback: Boolean
    :rtype: string
    '''
    locale = _parse_and_split_languageId(languageId=languageIdQuery,
                                         scriptId=scriptIdQuery,
                                         territoryId=territoryIdQuery)
    languageIdQuery = locale.language
    scriptIdQuery = locale.script
    territoryIdQuery = locale.territory
    if territoryId in _territories_db:
        if languageIdQuery and scriptIdQuery and territoryIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
            if icuLocaleIdQuery in _territories_db[territoryId].names:
                return _territories_db[territoryId].names[icuLocaleIdQuery]
        if languageIdQuery and scriptIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
            if icuLocaleIdQuery in _territories_db[territoryId].names:
                return _territories_db[territoryId].names[icuLocaleIdQuery]
        if languageIdQuery and territoryIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
            if icuLocaleIdQuery in _territories_db[territoryId].names:
                return _territories_db[territoryId].names[icuLocaleIdQuery]
        fallback_changes_main_script = False
        if scriptIdQuery:
            old_main_script = list_scripts(
                languageId=languageIdQuery+'_'+scriptIdQuery)[:1]
            new_main_script = list_scripts(
                languageId=languageIdQuery)[:1]
            if old_main_script != new_main_script:
                fallback_changes_main_script = True
        if languageIdQuery and not fallback_changes_main_script:
            icuLocaleIdQuery = languageIdQuery
            if icuLocaleIdQuery in _territories_db[territoryId].names:
                return _territories_db[territoryId].names[icuLocaleIdQuery]
        if fallback and 'en' in _territories_db[territoryId].names:
            return _territories_db[territoryId].names['en']
    return ''

def language_name(languageId = None, scriptId = None, territoryId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None, fallback=True):
    '''Query translations of language names

    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :param languageIdQuery: identifier for the language used in the result
    :type languageIdQuery: string
    :param scriptIdQuery: identifier for the script used in the result
    :type scriptIdQuery: string
    :param territoryIdQuery: identifier for the territory used in the result
    :type territoryIdQuery: string
    :param fallback: Whether a fallback to English should be returned if the
                     name cannot be found in the requested language.
    :type fallback: Boolean
    :rtype: string

    **Examples:**

    >>> print(language_name(languageId="sr"))
    Српски

    I.e. the endonym for “Serbian” in the default Cyrillic script is
    “српски”.

    If the script “Cyrl” is supplied as well, the name of the
    script is added for clarity:

    >>> print(language_name(languageId="sr", scriptId="Cyrl"))
    Српски (Ћирилица)

    And in Latin script the endonym is:

    >>> print(language_name(languageId="sr", scriptId="Latn"))
    Srpski (Latinica)

    And “Serbian” translated to English is:

    >>> print(language_name(languageId="sr", languageIdQuery="en"))
    Serbian

    And with adding the script information:

    >>> print(language_name(languageId="sr", scriptId="Cyrl", languageIdQuery="en"))
    Serbian (Cyrillic)

    >>> print(language_name(languageId="sr", scriptId="Latn", languageIdQuery="en"))
    Serbian (Latin)

    >>> print(language_name(languageId="de_DE", languageIdQuery="en"))
    German (Germany)

    >>> print(language_name(languageId="es_419", languageIdQuery="en"))
    Spanish (Latin America)

    >>> print(language_name(languageId="ca_ES"))
    Català (Espanya)

    >>> print(language_name(languageId="ca_ES.UTF-8"))
    Català (Espanya)

    >>> print(language_name(languageId="ca_ES@valencia"))
    Valencià (Espanya)

    >>> print(language_name(languageId="ca_ES.utf8@valencia"))
    Valencià (Espanya)

    >>> print(language_name(languageId="ca_ES.utf8@valencia"))
    Valencià (Espanya)

    >>> print(language_name(languageId="ca_ES.utf8@valencia", languageIdQuery='de'))
    Valencianisch (Spanien)

    >>> print(language_name(languageId="ca_ES.utf8@valencia", languageIdQuery='en'))
    Valencian (Spain)
    '''
    return _capitalize_name(
        _language_name(languageId=languageId,
                        scriptId=scriptId,
                        territoryId=territoryId,
                        languageIdQuery=languageIdQuery,
                        scriptIdQuery=scriptIdQuery,
                        territoryIdQuery=territoryIdQuery,
                        fallback=fallback),
        languageId=languageId,
        scriptId=scriptId,
        territoryId=territoryId,
        languageIdQuery=languageIdQuery,
        scriptIdQuery=scriptIdQuery,
        territoryIdQuery=territoryIdQuery)

def _language_name(languageId = None, scriptId = None, territoryId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None, fallback=True):
    '''Internal function to query translations of language names

    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :param languageIdQuery: identifier for the language used in the result
    :type languageIdQuery: string
    :param scriptIdQuery: identifier for the script used in the result
    :type scriptIdQuery: string
    :param territoryIdQuery: identifier for the territory used in the result
    :type territoryIdQuery: string
    :param fallback: Whether a fallback to English should be returned if the
                     name cannot be found in the requested language.
    :type fallback: Boolean
    :rtype: string
    '''
    if not languageId:
        return ''
    icuLocaleId = ''
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    localeQuery = _parse_and_split_languageId(languageId=languageIdQuery,
                                              scriptId=scriptIdQuery,
                                              territoryId=territoryIdQuery)
    languageIdQuery = localeQuery.language
    scriptIdQuery = localeQuery.script
    territoryIdQuery = localeQuery.territory
    if not languageIdQuery:
        # get the endonym
        languageIdQuery = languageId
        scriptIdQuery = scriptId
        territoryIdQuery = territoryId
    if languageId and scriptId and territoryId:
        icuLocaleId = languageId+'_'+scriptId+'_'+territoryId
        if icuLocaleId in _languages_db:
            if languageIdQuery and scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery and scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
    if languageId and scriptId:
        icuLocaleId = languageId+'_'+scriptId
        if icuLocaleId in _languages_db:
            cname = territory_name(territoryId=territoryId,
                                   languageIdQuery=languageIdQuery,
                                   scriptIdQuery=scriptIdQuery,
                                   territoryIdQuery=territoryIdQuery)
            if languageIdQuery and  scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    lname = _languages_db[icuLocaleId].names[icuLocaleIdQuery]
                    if cname:
                        return lname + ' ('+cname+')'
                    return lname
            if languageIdQuery and  scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    lname = _languages_db[icuLocaleId].names[icuLocaleIdQuery]
                    if cname:
                        return lname + ' ('+cname+')'
                    return lname
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    lname = _languages_db[icuLocaleId].names[icuLocaleIdQuery]
                    if cname:
                        return lname + ' ('+cname+')'
                    return lname
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    lname = _languages_db[icuLocaleId].names[icuLocaleIdQuery]
                    if cname:
                        return lname + ' ('+cname+')'
                    return lname
    if languageId and territoryId:
        icuLocaleId = languageId+'_'+territoryId
        if icuLocaleId in _languages_db:
            if languageIdQuery and  scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery and  scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                    return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
        if locale.variant not in ('VALENCIA',):
            # Don’t do this if locale variant is VALENCIA
            # because then this will run into endless recursion:
            lname = language_name(languageId=languageId,
                                  languageIdQuery=languageIdQuery,
                                  scriptIdQuery=scriptIdQuery,
                                  territoryIdQuery=territoryIdQuery)
            cname = territory_name(territoryId=territoryId,
                                 languageIdQuery=languageIdQuery,
                                 scriptIdQuery=scriptIdQuery,
                                 territoryIdQuery=territoryIdQuery)
            if lname and cname:
                return lname + ' ('+cname+')'
    icuLocaleId = languageId
    if icuLocaleId in _languages_db:
        if languageIdQuery and  scriptIdQuery and territoryIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
            if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
        if languageIdQuery and  scriptIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
            if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
        if languageIdQuery and territoryIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
            if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
        fallback_changes_main_script = False
        if scriptIdQuery:
            old_main_script = list_scripts(
                languageId=languageIdQuery+'_'+scriptIdQuery)[:1]
            new_main_script = list_scripts(
                languageId=languageIdQuery)[:1]
            if old_main_script != new_main_script:
                fallback_changes_main_script = True
        if languageIdQuery and not fallback_changes_main_script:
            icuLocaleIdQuery = languageIdQuery
            if icuLocaleIdQuery in _languages_db[icuLocaleId].names:
                return _languages_db[icuLocaleId].names[icuLocaleIdQuery]
    if (fallback
        and icuLocaleId
        and icuLocaleId in _languages_db
        and 'en' in _languages_db[icuLocaleId].names):
        return _languages_db[icuLocaleId].names['en']
    return ''

def _timezone_name_from_id_parts(timezoneId = None, icuLocaleIdQuery = None):
    '''Query translation of timezone IDs by querying translations
    for each part of the ID seperately and putting the results together
    '''
    if not (timezoneId and icuLocaleIdQuery):
        return ''
    timezoneId_parts = timezoneId.split('/')
    part_names = []
    for timezoneId_part in timezoneId_parts:
        if timezoneId_part not in _timezoneIdParts_db:
            part_names.append(timezoneId_part)
            continue
        if icuLocaleIdQuery in _timezoneIdParts_db[timezoneId_part].names:
            name = _timezoneIdParts_db[timezoneId_part].names[icuLocaleIdQuery]
            if name:
                part_names.append(name)
        elif icuLocaleIdQuery == 'en':
            name = timezoneId_part.replace('_', ' ')
            part_names.append(name)
    if len(part_names) == len(timezoneId_parts):
        return '/'.join(part_names)
    return ''

def _timezone_name(timezoneId = None, icuLocaleIdQuery = None):
    '''
    Internal helper function to translate timezone IDs
    '''
    if not (timezoneId and icuLocaleIdQuery):
        return ''
    if timezoneId in _timezones_db:
        if icuLocaleIdQuery in _timezones_db[timezoneId].names:
            return _timezones_db[timezoneId].names[icuLocaleIdQuery]
    name_from_parts = _timezone_name_from_id_parts(
        timezoneId=timezoneId, icuLocaleIdQuery=icuLocaleIdQuery)
    if name_from_parts:
        return name_from_parts
    return ''

def timezone_name(timezoneId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None):
    '''Query translations of timezone IDs

    :param timezoneId: identifier for the time zone
    :type timezoneId: string
    :param languageIdQuery: identifier for the language used in the result
    :type languageIdQuery: string
    :param scriptIdQuery: identifier for the script used in the result
    :type scriptIdQuery: string
    :param territoryIdQuery: identifier for the territory used in the result
    :type territoryId: string
    :rtype: string

    **Examples:**

    >>> print(timezone_name(timezoneId='US/Pacific', languageIdQuery='ja'))
    アメリカ合衆国/太平洋時間

    If no translation can be found, the timezone ID is returned
    unchanged:

    >>> print(timezone_name(timezoneId='Pacific/Pago_Pago', languageIdQuery='xxx'))
    Pacific/Pago_Pago
    '''
    locale = _parse_and_split_languageId(languageId=languageIdQuery,
                                         scriptId=scriptIdQuery,
                                         territoryId=territoryIdQuery)
    languageIdQuery = locale.language
    scriptIdQuery = locale.script
    territoryIdQuery = locale.territory
    if languageIdQuery and scriptIdQuery and territoryIdQuery:
        name = _timezone_name(
            timezoneId=timezoneId,
            icuLocaleIdQuery=languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery)
        if name:
            return name
    if languageIdQuery and scriptIdQuery:
        name = _timezone_name(
            timezoneId=timezoneId,
            icuLocaleIdQuery=languageIdQuery+'_'+scriptIdQuery)
        if name:
            return name
    if languageIdQuery and territoryIdQuery:
        name = _timezone_name(
            timezoneId=timezoneId,
            icuLocaleIdQuery=languageIdQuery+'_'+territoryIdQuery)
        if name:
            return name
    if languageIdQuery:
        name = _timezone_name(
            timezoneId=timezoneId,
            icuLocaleIdQuery=languageIdQuery)
        if name:
            return name
    return timezoneId

def territoryId(territoryName = ''):
    '''Query the territoryId from a translated name of a territory.

    :param territoryName: the translated name of a language
    :type territoryName: string
    :rtype: string

    The translated name given should be a Python Unicode string or an
    UTF-8 encoded string.

    The translated name can be in any language. But there will be only
    a result if the translation matches exactly.

    **Examples:**

    >>> territoryId("India")
    'IN'

    >>> territoryId("भारत")
    'IN'

    >>> territoryId("インド")
    'IN'

    >>> territoryId("Latin America")
    '419'

    >>> territoryId("Latinoamérica")
    '419'

    '''
    if not territoryName:
        return ''
    if not isinstance(territoryName, str):
        territoryName = territoryName.decode('UTF-8')
    for territoryId, territory_item in _territories_db.items():
        for name in territory_item.names.values():
            if territoryName == name:
                return territoryId
    return ''

def languageId(languageName = ''):
    '''Query the languageId from a translated name of a language.

    :param languageName: the translated name of a language
    :type languageName: string
    :rtype: string

    The translated name given should be a Python Unicode string or an
    UTF-8 encoded string.

    The translated name can be in any language. But there will be only
    a result if the translation matches exactly.

    **Examples:**

    >>> languageId("Marathi")
    'mr'

    >>> languageId("मराठी")
    'mr'

    >>> languageId("マラーティー語")
    'mr'

    '''
    if not languageName:
        return ''
    if not isinstance(languageName, str):
        languageName = languageName.decode('UTF-8')
    for languageId, language_item in _languages_db.items():
        for name in language_item.names.values():
            if languageName.lower() == name.lower():
                return languageId
    language_territory_pattern = re.compile(
        r'^(?P<language_name>[^()]+)[\s]+[(](?P<territory_name>[^()]+)[)]',
        re.MULTILINE|re.UNICODE)
    match = language_territory_pattern.search(languageName)
    if match:
        language_name = match.group('language_name')
        territory_name = match.group('territory_name')
        for languageId, language_item in _languages_db.items():
            for language_item_name in language_item.names.values():
                if language_name.lower() == language_item_name.lower():
                    for territoryId, territory_item in _territories_db.items():
                        for territory_item_name in territory_item.names.values():
                            if territory_name.lower() == territory_item_name.lower():
                                return languageId+'_'+territoryId

    return ''

extra_bonus = 1000000

def list_locales(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    '''List suitable glibc locales

    :param concise: if True, return only to highly ranked results
    :type concise: boolean
    :param show_weights: Also return the weights used in the ranking
    :type show_weights: boolean
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :rtype: a list of strings

    **Examples:**

    List the suitable locales for the language “German”:

    >>> list_locales(languageId="de")
    ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']

    So this returns a list of locales for German. These lists are
    sorted in order of decreasing likelyhood, i.e. the most common
    value comes first.

    One can also list the possible locales for the territory “Switzerland”:

    >>> list_locales(territoryId="CH")
    ['de_CH.UTF-8', 'fr_CH.UTF-8', 'it_CH.UTF-8', 'wae_CH.UTF-8']


    If one knows both, the language “German” and the territory
    “Switzerland”, the result is unique:

    >>> list_locales(languageId="de", territoryId="CH")
    ['de_CH.UTF-8']

    '''
    ranked_locales = {}
    skipTerritory = False
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in _languages_db:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 100
    if languageId in _languages_db:
        for locale in _languages_db[languageId].locales:
            if _languages_db[languageId].locales[locale] != 0:
                if locale not in ranked_locales:
                    ranked_locales[locale] = _languages_db[languageId].locales[locale]
                else:
                    ranked_locales[locale] *= _languages_db[languageId].locales[locale]
                    ranked_locales[locale] *= extra_bonus
                ranked_locales[locale] *= language_bonus
    territory_bonus = 1
    if territoryId in _territories_db and not skipTerritory:
        for locale in _territories_db[territoryId].locales:
            if _territories_db[territoryId].locales[locale] != 0:
                if locale not in ranked_locales:
                    ranked_locales[locale] = _territories_db[territoryId].locales[locale]
                else:
                    ranked_locales[locale] *= _territories_db[territoryId].locales[locale]
                    ranked_locales[locale] *= extra_bonus
                ranked_locales[locale] *= territory_bonus
    ranked_list = _dictionary_to_ranked_list(ranked_locales)
    if concise:
        ranked_list = _make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    return _ranked_list_to_list(ranked_list)

def list_common_languages():
    '''List common languages

    derived from GNOME/gnome-control-center
        panels/common/cc-common-language.c
        cc_common_language_get_initial_languages

    which is based on number of speakers.

    **Examples:**

    >>> list_common_languages()
    ['ar', 'en', 'fr', 'de', 'ja', 'zh', 'ru', 'es']

    '''

    common_locales = []
    common_locales.append("ar_EG.UTF-8")
    common_locales.append("en_US.UTF-8")
    common_locales.append("fr_FR.UTF-8")
    common_locales.append("de_DE.UTF-8")
    common_locales.append("ja_JP.UTF-8")
    common_locales.append("zh_CN.UTF-8")
    common_locales.append("ru_RU.UTF-8")
    common_locales.append("es_ES.UTF-8")

    languages = map(parse_locale, common_locales)
    return [lang.language for lang in languages]

def list_scripts(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    '''List scripts used for a language and/or in a territory

    :param concise: if True, return only to highly ranked results
    :type concise: boolean
    :param show_weights: Also return the weights used in the ranking
    :type show_weights: boolean
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :rtype: a list of strings

    Returns a list of ISO-15924 script ids:

    https://en.wikipedia.org/wiki/ISO_15924

    **Examples:**

    List the suitable scripts for the language “Serbian”:

    >>> list_scripts(languageId="sr")
    ['Cyrl', 'Latn']

    So this returns a list of scripts which are in use for
    Serbian. These lists are sorted in order of decreasing likelyhood,
    i.e. the most common value comes first.

    List the suitable scripts for the language “Punjabi”:

    >>> list_scripts(languageId="pa")
    ['Guru', 'Arab']

    One can also list the possible scripts for a territory like
    “Pakistan”:

    >>> list_scripts(territoryId="PK")
    ['Arab']

    If one knows both, the language “Punjabi” and the territory
    “Pakistan” or “India”, one can find out which script is the
    preferred one:

    >>> list_scripts(languageId="pa", territoryId="PK")
    ['Arab']

    So the preferred script for Punjabi in Pakistan is “Arab”

    >>> list_scripts(languageId="pa", territoryId="IN")
    ['Guru', 'Arab']

    and the preferred script for Punjabi in India is “Guru”.

    '''
    ranked_scripts = {}
    skipTerritory = False
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    if scriptId:
        # scriptId is already given in the input, just return it:
        return [scriptId]
    if languageId and territoryId and languageId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 100
    if languageId in _languages_db:
        for script in _languages_db[languageId].scripts:
            if _languages_db[languageId].scripts[script] != 0:
                if script not in ranked_scripts:
                    ranked_scripts[script] = _languages_db[languageId].scripts[script]
                else:
                    ranked_scripts[script] *= _languages_db[languageId].scripts[script]
                    ranked_scripts[script] *= extra_bonus
                ranked_scripts[script] *= language_bonus
    territory_bonus = 1
    if territoryId in _territories_db and not skipTerritory:
        for script in _territories_db[territoryId].scripts:
            if _territories_db[territoryId].scripts[script] != 0:
                if script not in ranked_scripts:
                    ranked_scripts[script] = _territories_db[territoryId].scripts[script]
                else:
                    ranked_scripts[script] *= _territories_db[territoryId].scripts[script]
                    ranked_scripts[script] *= extra_bonus
                ranked_scripts[script] *= territory_bonus
    ranked_list = _dictionary_to_ranked_list(ranked_scripts)
    if concise:
        ranked_list = _make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    return _ranked_list_to_list(ranked_list)

def list_inputmethods(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    '''List suitable input methods

    :param concise: if True, return only to highly ranked results
    :type concise: boolean
    :param show_weights: Also return the weights used in the ranking
    :type show_weights: boolean
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :rtype: a list of strings

    **Examples:**

    List the suitable input methods for the language “Japanese”:

    >>> list_inputmethods(languageId="ja")
    ['ibus/anthy', 'ibus/kkc']

    So this returns a list of input methods for Japanese. These lists are
    sorted in order of decreasing likelyhood, i.e. the most common
    value comes first.

    One can also list the possible input methods for the territory “Japan”:

    >>> list_inputmethods(territoryId="JP")
    ['ibus/anthy', 'ibus/kkc']
    '''
    ranked_inputmethods = {}
    skipTerritory = False
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in _languages_db:
        languageId = languageId+'_'+scriptId
        skipTerritory = True
    elif languageId and territoryId and languageId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 100
    if languageId in _languages_db:
        for inputmethod in _languages_db[languageId].inputmethods:
            if _languages_db[languageId].inputmethods[inputmethod] != 0:
                if inputmethod not in ranked_inputmethods:
                    ranked_inputmethods[inputmethod] = _languages_db[languageId].inputmethods[inputmethod]
                else:
                    ranked_inputmethods[inputmethod] *= _languages_db[languageId].inputmethods[inputmethod]
                    ranked_inputmethods[inputmethod] *= extra_bonus
                ranked_inputmethods[inputmethod] *= language_bonus
    territory_bonus = 1
    if territoryId in _territories_db and not skipTerritory:
        for inputmethod in _territories_db[territoryId].inputmethods:
            if _territories_db[territoryId].inputmethods[inputmethod] != 0:
                if inputmethod not in ranked_inputmethods:
                    ranked_inputmethods[inputmethod] = _territories_db[territoryId].inputmethods[inputmethod]
                else:
                    ranked_inputmethods[inputmethod] *= _territories_db[territoryId].inputmethods[inputmethod]
                    ranked_inputmethods[inputmethod] *= extra_bonus
                ranked_inputmethods[inputmethod] *= territory_bonus
    ranked_list = _dictionary_to_ranked_list(ranked_inputmethods)
    if concise:
        ranked_list = _make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    return _ranked_list_to_list(ranked_list)

def list_keyboards(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    '''List likely X11 keyboard layouts

    :param concise: if True, return only to highly ranked results
    :type concise: boolean
    :param show_weights: Also return the weights used in the ranking
    :type show_weights: boolean
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :rtype: a list of strings

    **Examples:**

    Listing likely X11 keyboard layouts for “German”:

    >>> list_keyboards(languageId="de")
    ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']

    Listing likely X11 keyboard layouts for “Switzerland”:

    >>> list_keyboards(territoryId="CH")
    ['ch', 'ch(fr)', 'it']

    When specifying both “German” *and* “Switzerland”, the
    returned X11 keyboard layout is unique:

    >>> list_keyboards(languageId="de", territoryId="CH")
    ['ch']
    '''
    ranked_keyboards = {}
    skipTerritory = False
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in _languages_db:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 1
    if languageId in _languages_db:
        for keyboard in _languages_db[languageId].keyboards:
            if _languages_db[languageId].keyboards[keyboard] != 0:
                if keyboard not in ranked_keyboards:
                    ranked_keyboards[keyboard] = _languages_db[languageId].keyboards[keyboard]
                else:
                    ranked_keyboards[keyboard] *= _languages_db[languageId].keyboards[keyboard]
                    ranked_keyboards[keyboard] *= extra_bonus
                ranked_keyboards[keyboard] *= language_bonus
    territory_bonus = 1
    if territoryId in _territories_db and not skipTerritory:
        for keyboard in _territories_db[territoryId].keyboards:
            if _territories_db[territoryId].keyboards[keyboard] != 0:
                if keyboard not in ranked_keyboards:
                    ranked_keyboards[keyboard] = _territories_db[territoryId].keyboards[keyboard]
                else:
                    ranked_keyboards[keyboard] *= _territories_db[territoryId].keyboards[keyboard]
                    ranked_keyboards[keyboard] *= extra_bonus
                ranked_keyboards[keyboard] *= territory_bonus
    ranked_list = _dictionary_to_ranked_list(ranked_keyboards)
    if concise:
        ranked_list = _make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    return _ranked_list_to_list(ranked_list)

def list_common_keyboards(languageId = None, scriptId = None, territoryId = None):
    # pylint: disable=line-too-long
    '''Returns highest ranked keyboard layout(s)
2
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :return: list of keyboard layouts
    :rtype: list of str(s)

    **Examples:**

    >>> list_common_keyboards()
    ['af(ps)', 'al', 'am', 'ara', 'au', 'az', 'ba', 'be(oss)', 'bg', 'br', 'bt', 'by', 'ca(eng)', 'ca(ike)', 'ch', 'cn', 'cn(ug)', 'cz', 'de(nodeadkeys)', 'dk', 'ee', 'es', 'es(ast)', 'es(cat)', 'et', 'fi', 'fo', 'fr(bre)', 'fr(oss)', 'gb', 'ge', 'gr', 'hr', 'hu', 'ie(CloGaelach)', 'il', 'in(eng)', 'ir', 'is', 'it', 'jp', 'ke', 'kg', 'kh', 'kr', 'kz', 'la', 'latam', 'lt', 'lv', 'ma(tifinagh)', 'mk', 'mm', 'mn', 'mt', 'mv', 'ng', 'ng(hausa)', 'ng(igbo)', 'ng(yoruba)', 'no', 'np', 'ph', 'pk', 'pl', 'pt', 'ro', 'rs', 'rs(latin)', 'ru', 'ru(bak)', 'ru(chm)', 'ru(cv)', 'ru(kom)', 'ru(os_winkeys)', 'ru(sah)', 'ru(tt)', 'ru(udm)', 'ru(xal)', 'se', 'si', 'sk', 'sn', 'syc', 'th', 'tj', 'tm', 'tr', 'tr(crh)', 'tr(ku)', 'tw', 'ua', 'us', 'us(altgr-intl)', 'us(euro)', 'us(intl)', 'uz', 'vn', 'za']
    >>> list_common_keyboards(languageId='fr')
    ['fr(oss)']
    >>> list_common_keyboards(territoryId='CA')
    ['ca(eng)']
    >>> list_common_keyboards(territoryId='FR')
    ['fr(oss)']
    >>> list_common_keyboards(languageId='fr', territoryId='CA')
    ['ca']
    >>> list_common_keyboards(languageId='de', territoryId='FR')
    ['fr(oss)']
    >>> list_common_keyboards(languageId='sr', scriptId='Latn')
    ['rs(latin)']
    >>> list_common_keyboards(languageId='zh', scriptId='Hans')
    ['cn']
    >>> list_common_keyboards(languageId='zh', scriptId='Hans', territoryId='TW')
    ['tw']
    '''
    # pylint: enable=line-too-long
    high_ranked_keyboards = []
    if not languageId and not scriptId and not territoryId:
        for _, language in _languages_db.items():
            keyboard_layouts = language.keyboards
            selected_layouts = [layout for layout, rank in keyboard_layouts.items()
                                if rank >= _KEYBOARD_LAYOUT_RANK_THRESHOLD]
            if selected_layouts:
                high_ranked_keyboards.extend(selected_layouts)
        high_ranked_keyboards = list(set(high_ranked_keyboards))

    kwargs = {}
    locale = _parse_and_split_languageId(
        languageId=languageId, scriptId=scriptId, territoryId=territoryId
    )
    if locale.language:
        kwargs.update({'languageId': locale.language})
    if locale.script:
        kwargs.update({'scriptId': locale.script})
    if locale.territory:
        kwargs.update({'territoryId': locale.territory})
    common_layouts = list_keyboards(**kwargs)
    if common_layouts:
        # Picking up first layout from the list
        high_ranked_keyboards.append(common_layouts[0])

    return sorted(high_ranked_keyboards)

def list_common_locales(languageId = None, scriptId = None, territoryId = None):
    '''Returns highest ranked locales

    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :return: list of locales
    :rtype: list of strings

    **Examples:**

    >>> list_common_locales()
    ['ar_EG.UTF-8', 'en_US.UTF-8', 'en_GB.UTF-8', 'fr_FR.UTF-8', 'de_DE.UTF-8', 'ja_JP.UTF-8', 'zh_CN.UTF-8', 'ru_RU.UTF-8', 'es_ES.UTF-8']

    >>> list_common_locales(languageId='fr')
    ['fr_FR.UTF-8']

    >>> list_common_locales(territoryId='CA')
    ['en_CA.UTF-8']

    >>> list_common_locales(territoryId='FR')
    ['fr_FR.UTF-8']

    >>> list_common_locales(languageId='fr', territoryId='CA')
    ['fr_CA.UTF-8']

    >>> list_common_locales(languageId='de', territoryId='FR')
    ['de_DE.UTF-8']

    >>> list_common_locales(languageId='sr', scriptId='Latn')
    ['sr_RS.UTF-8@latin']

    >>> list_common_locales(languageId='sr', scriptId='Cyrl')
    ['sr_RS.UTF-8']

    >>> list_common_locales(languageId='zh', scriptId='Hans')
    ['zh_CN.UTF-8']

    >>> list_common_locales(languageId='zh', scriptId='Hant')
    ['zh_TW.UTF-8']

    >>> list_common_locales(languageId='zh', territoryId='TW')
    ['zh_TW.UTF-8']
    '''
    high_ranked_locales = []
    if not languageId and not scriptId and not territoryId:
        for language in list_common_languages():
            locales = _languages_db[language].locales
            selected_locales = [locale for locale, rank
                                in sorted(locales.items(),
                                          key=lambda x: (-x[1]))
                                if rank >= _LOCALE_RANK_THRESHOLD]
            if selected_locales:
                high_ranked_locales.extend(selected_locales)
        return high_ranked_locales

    kwargs = {}
    locale = _parse_and_split_languageId(
        languageId=languageId, scriptId=scriptId, territoryId=territoryId
    )
    if locale.language:
        kwargs.update({'languageId': locale.language})
    if locale.script:
        kwargs.update({'scriptId': locale.script})
    if locale.territory:
        kwargs.update({'territoryId': locale.territory})
    common_locales = list_locales(**kwargs)
    if common_locales:
        # Picking up first locale from the list
        high_ranked_locales.append(common_locales[0])
    return high_ranked_locales

def list_consolefonts(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    '''List likely Linux Console fonts

    :param concise: if True, return only to highly ranked results
    :type concise: boolean
    :param show_weights: Also return the weights used in the ranking
    :type show_weights: boolean
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :rtype: a list of strings

    **Examples:**

    Listing likely console fonts  for English:

    >>> list_consolefonts(languageId="en")
    ['eurlatgr']

    Listing likely console fonts for Greek:

    >>> list_consolefonts(languageId="el")
    ['eurlatgr', 'iso07u-16', 'LatGrkCyr-8x16']

    Listing likely console fonts for Greece:

    >>> list_consolefonts(territoryId="GR")
    ['eurlatgr', 'iso07u-16', 'LatGrkCyr-8x16']

    Listing likely console fonts for Greek in Greece:

    list_consolefonts(languageId="el", territoryId="GR")
    ['eurlatgr']

    Listing likely console fonts for Greek in a non-Greek country like
    the UK (the language has higher weight):

    >>> list_consolefonts(languageId="el", territoryId="GB")
    ['eurlatgr']

    Listing likely console fonts for Russian in Russia:

    >>> list_consolefonts(languageId="ru", territoryId="RU")
    ['latarcyrheb-sun16']

    Listing likely console fonts for Russian in a non-Russian country like
    the UK (the language has higher weight):

    >>> list_consolefonts(languageId="ru", territoryId="GB")
    ['latarcyrheb-sun16', 'eurlatgr']

    '''
    ranked_consolefonts = {}
    skipTerritory = False
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in _languages_db:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 100
    if languageId in _languages_db:
        for consolefont in _languages_db[languageId].consolefonts:
            if _languages_db[languageId].consolefonts[consolefont] != 0:
                if consolefont not in ranked_consolefonts:
                    ranked_consolefonts[consolefont] = _languages_db[languageId].consolefonts[consolefont]
                else:
                    ranked_consolefonts[consolefont] *= _languages_db[languageId].consolefonts[consolefont]
                    ranked_consolefonts[consolefont] *= extra_bonus
                ranked_consolefonts[consolefont] *= language_bonus
    territory_bonus = 1
    if territoryId in _territories_db and not skipTerritory:
        for consolefont in _territories_db[territoryId].consolefonts:
            if _territories_db[territoryId].consolefonts[consolefont] != 0:
                if consolefont not in ranked_consolefonts:
                    ranked_consolefonts[consolefont] = _territories_db[territoryId].consolefonts[consolefont]
                else:
                    ranked_consolefonts[consolefont] *= _territories_db[territoryId].consolefonts[consolefont]
                    ranked_consolefonts[consolefont] *= extra_bonus
                ranked_consolefonts[consolefont] *= territory_bonus
    ranked_list = _dictionary_to_ranked_list(ranked_consolefonts)
    if concise:
        ranked_list = _make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    return _ranked_list_to_list(ranked_list)

def list_timezones(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    '''List likely timezones

    :param concise: if True, return only to highly ranked results
    :type concise: boolean
    :param show_weights: Also return the weights used in the ranking
    :type show_weights: boolean
    :param languageId: identifier for the language
    :type languageId: string
    :param scriptId: identifier for the script
    :type scriptId: string
    :param territoryId: identifier for the territory
    :type territoryId: string
    :rtype: a list of strings

    **Examples:**

    >>> list_timezones(territoryId="DE")
    ['Europe/Berlin']

    >>> list_timezones(languageId="de")
    ['Europe/Berlin', 'Europe/Vienna', 'Europe/Zurich', 'Europe/Brussels', 'Europe/Luxembourg']

    >>> list_timezones(territoryId="CH")
    ['Europe/Zurich']

    >>> list_timezones(languageId="fr", territoryId="CH")
    ['Europe/Zurich']

    >>> list_timezones(languageId="fr")
    ['Europe/Paris', 'America/Montreal', 'Europe/Brussels', 'Europe/Zurich', 'Europe/Luxembourg']

    The territory gets more weight than the language:

    >>> list_timezones(languageId="ja", territoryId="CH")
    ['Europe/Zurich', 'Asia/Tokyo']
    '''
    ranked_timezones = {}
    skipTerritory = False
    locale = _parse_and_split_languageId(languageId=languageId,
                                         scriptId=scriptId,
                                         territoryId=territoryId)
    languageId = locale.language
    scriptId = locale.script
    territoryId = locale.territory
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in _languages_db:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in _languages_db:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 1
    if languageId in _languages_db:
        for timezone in _languages_db[languageId].timezones:
            if _languages_db[languageId].timezones[timezone] != 0:
                if timezone not in ranked_timezones:
                    ranked_timezones[timezone] = _languages_db[languageId].timezones[timezone]
                else:
                    ranked_timezones[timezone] *= _languages_db[languageId].timezones[timezone]
                    ranked_timezones[timezone] *= extra_bonus
                ranked_timezones[timezone] *= language_bonus
    territory_bonus = 100
    if territoryId in _territories_db and not skipTerritory:
        for timezone in _territories_db[territoryId].timezones:
            if _territories_db[territoryId].timezones[timezone] != 0:
                if timezone not in ranked_timezones:
                    ranked_timezones[timezone] = _territories_db[territoryId].timezones[timezone]
                else:
                    ranked_timezones[timezone] *= _territories_db[territoryId].timezones[timezone]
                    ranked_timezones[timezone] *= extra_bonus
                ranked_timezones[timezone] *= territory_bonus
    ranked_list = _dictionary_to_ranked_list(ranked_timezones)
    if concise:
        ranked_list = _make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    return _ranked_list_to_list(ranked_list)

def list_all_languages() -> List[str]:
    '''
    List all language ids langtable knows something about
    '''
    return sorted(_languages_db.keys())

def list_all_locales() -> List[str]:
    '''
    List all (glibc style) locales langtable knows something about
    '''
    all_locales = set()
    for (_key, item) in _languages_db.items():
        all_locales.update(item.locales)
    for (_key, item) in _territories_db.items():
        all_locales.update(item.locales)
    return sorted(all_locales)

def list_all_keyboards() -> List[str]:
    '''
    List all keyboards langtable knows something about
    '''
    return sorted(_keyboards_db.keys())

def list_all_territories() -> List[str]:
    '''
    List all territory ids langtable knows something about
    '''
    return sorted(_territories_db.keys())

def list_all_timezones() -> List[str]:
    '''
    List all timezone ids langtable knows something about
    '''
    all_timezones = set()
    all_timezones.update(list(_timezones_db.keys()))
    for (_key, item) in _languages_db.items():
        all_timezones.update(item.timezones)
    for (_key, item) in _territories_db.items():
        all_timezones.update(item.timezones)
    return sorted(all_timezones)

def list_all_scripts() -> List[str]:
    '''
    List all script ids langtable knows something about
    '''
    all_scripts = set()
    for (_key, item) in _languages_db.items():
        all_scripts.update(item.scripts)
    for (_key, item) in _territories_db.items():
        all_scripts.update(item.scripts)
    return sorted(all_scripts)

def list_all_input_methods() -> List[str]:
    '''
    List all input methods langtable knows something about
    '''
    all_inputmethods = set()
    for (_key, item) in _languages_db.items():
        all_inputmethods.update(item.inputmethods)
    for (_key, item) in _territories_db.items():
        all_inputmethods.update(item.inputmethods)
    return sorted(all_inputmethods)

def list_all_console_fonts() -> List[str]:
    '''
    List all console fonts langtable knows something about
    '''
    all_consolefonts = set()
    for (_key, item) in _languages_db.items():
        all_consolefonts.update(item.consolefonts)
    for (_key, item) in _territories_db.items():
        all_consolefonts.update(item.consolefonts)
    return sorted(all_consolefonts)

def supports_ascii(keyboardId=None):
    '''Check whether a keyboard layout supports ASCII

    :param keyboardId: identifier for the keyboard
    :type keyboardId: string
    :rtype: string

    Returns True if the keyboard layout with that id can be used to
    type ASCII, returns false if the keyboard layout can not be used
    to type ASCII or if typing ASCII with that keyboard layout is
    difficult.

    **Examples:**

    >>> supports_ascii("jp")
    True
    >>> supports_ascii("ru")
    False
    '''
    if keyboardId in _keyboards_db:
        return _keyboards_db[keyboardId].ascii
    return True

def version():
    '''
    Return version of langtable
    '''
    # pkg_resources is part of setuptools
    import pkg_resources  # type: ignore pylint: disable=import-outside-toplevel
    return pkg_resources.require("langtable")[0].version

def info():
    '''
    Print some info about langtable
    '''
    # pkg_resources is part of setuptools
    import pkg_resources  # type: ignore pylint: disable=import-outside-toplevel
    project_name = pkg_resources.require("langtable")[0].project_name
    version = pkg_resources.require("langtable")[0].version
    module_path = pkg_resources.require("langtable")[0].module_path
    print(f'Project name: = {project_name}')
    print(f'Version: = {version}')
    print(f'Module path: = {module_path}')
    print(f'Loaded from: {os.path.realpath(__file__)}')
    print(f'Data files read: {_INFO["data_files_read"]}')

def _test_cldr_locale_pattern(localeId):
    '''
    Internal test function, do not use this.
    '''
    match = _cldr_locale_pattern.match(localeId)
    if match:
        return [('language', match.group('language')), ('script', match.group('script')), ('territory', match.group('territory'))]
    return []

def _test_language_territory(show_weights=False, languageId=None, scriptId=None, territoryId=None):
    '''
    Internal test function, do not use this.
    '''
    print(str(languageId)+": "
          +repr(list_locales(show_weights=show_weights,languageId=languageId))
          +'\n'
          +str(territoryId)+": "
          +repr(list_locales(show_weights=show_weights,territoryId=territoryId))
          +'\n'
          +" +: "
          +repr(list_locales(show_weights=show_weights,languageId=languageId,scriptId=scriptId,territoryId=territoryId))
          +'\n'
          +str(languageId)+": "
          +repr(list_keyboards(show_weights=show_weights,languageId=languageId))
          +'\n'
          +str(territoryId)+": "
          +repr(list_keyboards(show_weights=show_weights,territoryId=territoryId))
          +'\n'
          +" +: "
          +repr(list_keyboards(show_weights=show_weights,languageId=languageId,scriptId=scriptId,territoryId=territoryId))
          )

def _init(debug=False, logfilename='/dev/null') -> None:

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(filename=logfilename,
                        filemode="w",
                        format="%(levelname)s: %(message)s",
                        level=log_level)

    _read_file('territories.xml', TerritoriesContentHandler())
    _read_file('languages.xml', LanguagesContentHandler())
    _read_file('keyboards.xml', KeyboardsContentHandler())
    _read_file('timezones.xml', TimezonesContentHandler())
    _read_file('timezoneidparts.xml', TimezoneIdPartsContentHandler())

# pylint: enable=invalid-name

class __ModuleInitializer: # pylint: disable=too-few-public-methods,invalid-name
    def __init__(self) -> None:
        _init()

    def __del__(self) -> None:
        return

__module_init = __ModuleInitializer()

if __name__ == "__main__":
    import doctest
    import sys
    _init()
    (FAILED, ATTEMPTED) = doctest.testmod()
    print(f'{ATTEMPTED} tests run. {ATTEMPTED - FAILED} passed and {FAILED} failed.')
    if FAILED:
        sys.exit(FAILED)
    print('All tests passed.')
    sys.exit(0)
