#!/usr/bin/python
# vim:fileencoding=utf-8:sw=4:et

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

import os
from lxml import etree

import langtable
from langtable import list_locales
from langtable import list_keyboards

opts = {}
opts['debug'] = False

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='langtable')
    parser.add_argument('-T', '--territoriesoutputfile',
                        nargs='?',
                        type=str,
                        default='./data/territories.xml.new',
                        help='territories output file, default is ./data/territories.xml.new')
    parser.add_argument('-K', '--keyboardsoutputfile',
                        nargs='?',
                        type=str,
                        default='./data/keyboards.xml.new',
                        help='keyboards file, default is ./data/keyboards.xml.new')
    parser.add_argument('-L', '--languagesoutputfile',
                        nargs='?',
                        type=str,
                        default='./data/languages.xml.new',
                        help='languages output file, default is ./data/languages.xml.new')
    parser.add_argument('-z', '--timezonesoutputfile',
                        nargs='?',
                        type=str,
                        default='./data/timezones.xml.new',
                        help='timezones output file, default is ./data/timezones.xml.new')
    parser.add_argument('-p', '--timezoneidpartsoutputfile',
                        nargs='?',
                        type=str,
                        default='./data/timezoneidparts.xml.new',
                        help='timezoneidparts output file, default is ./data/timezoneidparts.xml.new')
    parser.add_argument('-l', '--logfilename',
                        nargs='?',
                        type=str,
                        default='./langtable.log',
                        help='log file, default is ./langtable.log')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='print debugging output')
    return parser.parse_args()

translations_languages = {}
translations_territories = {}
translations_timezone_cities = {}

def read_translations_from_cldr_file(file = None):
    translations_languages.clear()
    translations_territories.clear()
    translations_timezone_cities.clear()
    if file:
        ldmlTree = etree.parse(file).getroot()
        if ldmlTree.tag != 'ldml':
            print "error: Wrong ldmlTree.tag=%(tag)s." %ldmlTree.tag
            exit(1)
        if len(ldmlTree):
            for element in ldmlTree:
                if element.tag == 'localeDisplayNames':
                    localeDisplayNamesTree = element
                    if len(localeDisplayNamesTree):
                        for element in localeDisplayNamesTree:
                            if element.tag == 'languages':
                                languagesTree = element
                                if len(languagesTree):
                                    for element in languagesTree:
                                        languageId = element.get('type')
                                        translation = element.text
                                        if not (element.get('alt') == 'short' and languageId in translations_languages):
                                            translations_languages[languageId] = translation
                            if element.tag == 'territories':
                                territoriesTree = element
                                if len(territoriesTree):
                                    for element in territoriesTree:
                                        territoryId = element.get('type')
                                        translation = element.text
                                        if not (element.get('alt') == 'short' and territoryId in translations_territories):
                                            translations_territories[territoryId] = translation
                if element.tag == 'dates':
                    datesTree = element
                    for element in datesTree:
                        if element.tag == 'timeZoneNames':
                            timeZoneNamesTree = element
                            if len(timeZoneNamesTree):
                                for element in timeZoneNamesTree:
                                    if element.tag == 'zone':
                                        zoneId = element.get('type')
                                        idParts = zoneId.split('/')
                                        if len(idParts):
                                            idPart = idParts[-1]
                                            zoneTree = element
                                            for element in zoneTree:
                                                if element.tag == 'exemplarCity':
                                                    cityTranslation = element.text
                                                    translations_timezone_cities[idPart] = cityTranslation
    return

def get_translations_from_cldr(main_cldr_dir = None):
    for target_language in sorted(langtable._languages_db):
        cldr_file = main_cldr_dir+'/'+target_language+'.xml'
        if not os.path.exists(cldr_file):
            continue
        read_translations_from_cldr_file(cldr_file)
        for language_to_translate in translations_languages:
            if language_to_translate in langtable._languages_db:
                if target_language not in langtable._languages_db[language_to_translate].names:
                    print "Missing: %(language_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'language_to_translate': language_to_translate,
                          'target_language': target_language,
                          'tr': translations_languages[language_to_translate].encode('UTF-8')}
                    langtable._languages_db[language_to_translate].names[target_language] = translations_languages[language_to_translate]
                elif translations_languages[language_to_translate] \
                     == langtable._languages_db[language_to_translate].names[target_language]:
                    if opts['debug']:
                        print "Identical: %(language_to_translate)s → %(target_language)s = %(tr)s" \
                            %{'language_to_translate': language_to_translate,
                              'target_language': target_language,
                              'tr': translations_languages[language_to_translate].encode('UTF-8')}
                else:
                    print "- %(language_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'language_to_translate': language_to_translate,
                          'target_language': target_language,
                          'tr': langtable._languages_db[language_to_translate].names[target_language].encode('UTF-8')}
                    print "+ %(language_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'language_to_translate': language_to_translate,
                          'target_language': target_language,
                          'tr': translations_languages[language_to_translate].encode('UTF-8')}
            else:
                if opts['debug']:
                    print "Not in langtable: %(language_to_translate)s" \
                        %{'language_to_translate': language_to_translate}
        for territory_to_translate in translations_territories:
            if territory_to_translate in langtable._territories_db:
                if target_language not in langtable._territories_db[territory_to_translate].names:
                    print "Missing: %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'territory_to_translate': territory_to_translate,
                          'target_language': target_language,
                          'tr': translations_territories[territory_to_translate].encode('UTF-8')}
                    langtable._territories_db[territory_to_translate].names[target_language] = translations_territories[territory_to_translate]
                elif translations_territories[territory_to_translate] \
                     == langtable._territories_db[territory_to_translate].names[target_language]:
                    if opts['debug']:
                        print "Identical: %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                            %{'territory_to_translate': territory_to_translate,
                              'target_language': target_language,
                              'tr': translations_territories[territory_to_translate].encode('UTF-8')}
                else:
                    print "- %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'territory_to_translate': territory_to_translate,
                          'target_language': target_language,
                          'tr': langtable._territories_db[territory_to_translate].names[target_language].encode('UTF-8')}
                    print "+ %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'territory_to_translate': territory_to_translate,
                          'target_language': target_language,
                          'tr': translations_territories[territory_to_translate].encode('UTF-8')}
            else:
                if opts['debug']:
                    print "Not in langtable: %(territory_to_translate)s" \
                        %{'territory_to_translate': territory_to_translate}
        for timezone_city_to_translate in translations_timezone_cities:
            if timezone_city_to_translate in langtable._timezoneIdParts_db:
                if target_language not in langtable._timezoneIdParts_db[timezone_city_to_translate].names:
                    print "Missing: %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'timezone_city_to_translate': timezone_city_to_translate,
                          'target_language': target_language,
                          'tr': translations_timezone_cities[timezone_city_to_translate].encode('UTF-8')}
                    langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language] = translations_timezone_cities[timezone_city_to_translate]
                elif translations_timezone_cities[timezone_city_to_translate] \
                     == langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language]:
                    if opts['debug']:
                        print "Identical: %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" \
                            %{'timezone_city_to_translate': timezone_city_to_translate,
                              'target_language': target_language,
                              'tr': translations_timezone_cities[timezone_city_to_translate].encode('UTF-8')}
                else:
                    print "- %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'timezone_city_to_translate': timezone_city_to_translate,
                          'target_language': target_language,
                          'tr': langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language].encode('UTF-8')}
                    print "+ %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'timezone_city_to_translate': timezone_city_to_translate,
                          'target_language': target_language,
                          'tr': translations_timezone_cities[timezone_city_to_translate].encode('UTF-8')}
    return

def main():
    args = parse_args()
    if args.debug:
        opts['debug'] = True
    else:
        opts['debug'] = False

    langtable._init(debug = True,
                    logfilename = args.logfilename,
                    datadir = './data')

    get_translations_from_cldr(main_cldr_dir='/local/mfabian/src/cldr-svn/trunk/common/main')

    langtable._write_files(territoriesfilename = args.territoriesoutputfile,
                           languagesfilename = args.languagesoutputfile,
                           keyboardsfilename = args.keyboardsoutputfile,
                           timezonesfilename = args.timezonesoutputfile,
                           timezoneidpartsfilename = args.timezoneidpartsoutputfile)


if __name__ == '__main__':
    main()
