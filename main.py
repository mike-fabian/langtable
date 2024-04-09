#!/usr/bin/python3
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
from langtable import timezone_name

opts = {}
opts['debug'] = False

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='langtable')
    parser.add_argument('-T', '--territoriesoutputfile',
                        nargs='?',
                        type=str,
                        default='./langtable/data/territories.xml.new',
                        help='territories output file, default is %(default)s')
    parser.add_argument('-K', '--keyboardsoutputfile',
                        nargs='?',
                        type=str,
                        default='./langtable/data/keyboards.xml.new',
                        help='keyboards file, default is %(default)s')
    parser.add_argument('-L', '--languagesoutputfile',
                        nargs='?',
                        type=str,
                        default='./langtable/data/languages.xml.new',
                        help='languages output file, default is %(default)s')
    parser.add_argument('-z', '--timezonesoutputfile',
                        nargs='?',
                        type=str,
                        default='./langtable/data/timezones.xml.new',
                        help='timezones output file, default is %(default)s')
    parser.add_argument('-p', '--timezoneidpartsoutputfile',
                        nargs='?',
                        type=str,
                        default='./langtable/data/timezoneidparts.xml.new',
                        help='timezoneidparts output file, default is %(default)s')
    parser.add_argument('-l', '--logfilename',
                        nargs='?',
                        type=str,
                        default='./langtable.log',
                        help='log file, default is %(default)s')
    parser.add_argument('-c', '--include_changes',
                        action='store_true',
                        default=False,
                        help='Also write changed translations, not only new translations, default is %(default)s.')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='print debugging output')
    return parser.parse_args()

translations_languages = {}
translations_territories = {}
translations_timezone_cities = {}
timezone_city_aliases = {
    'Calcutta': 'Kolkata',
    'Asmera': 'Asmara',
    'Coral_Harbour': 'Atikokan',
    'Truk': 'Chuuk',
    'Faeroe': 'Faroe',
    'Saigon': 'Ho_Chi_Minh',
    'Katmandu': 'Kathmandu',
    'Ponape': 'Pohnpei',
}

def read_translations_from_cldr_file(file = None):
    translations_languages.clear()
    translations_territories.clear()
    translations_timezone_cities.clear()
    if file:
        ldmlTree = etree.parse(file).getroot()
        if ldmlTree.tag != 'ldml':
            print("error: Wrong ldmlTree.tag=%(tag)s." %ldmlTree.tag)
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
                                        if not (element.get('alt') in ['menu', 'short', 'variant'] and languageId in translations_languages):
                                            translations_languages[languageId] = translation
                            if element.tag == 'territories':
                                territoriesTree = element
                                if len(territoriesTree):
                                    for element in territoriesTree:
                                        territoryId = element.get('type')
                                        translation = element.text
                                        if not (element.get('alt') in ['menu', 'short', 'variant'] and territoryId in translations_territories):
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
    for alias in timezone_city_aliases:
        if alias in translations_timezone_cities:
            translations_timezone_cities[timezone_city_aliases[alias]] = translations_timezone_cities[alias]
    return

def get_translations_from_cldr(main_cldr_dir = None, include_changes=False):
    for target_language in sorted(langtable._languages_db):
        cldr_file = main_cldr_dir+'/'+target_language+'.xml'
        if not os.path.exists(cldr_file):
            continue
        read_translations_from_cldr_file(cldr_file)
        for language_to_translate in translations_languages:
            if translations_languages[language_to_translate] in ('↑↑↑', 'Tagalog'):
                continue
            if language_to_translate in langtable._languages_db:
                if target_language not in langtable._languages_db[language_to_translate].names:
                    print("Missing: %(language_to_translate)s → %(target_language)s = %(tr)s" %{
                        'language_to_translate': language_to_translate,
                        'target_language': target_language,
                        'tr': translations_languages[language_to_translate]})
                    langtable._languages_db[language_to_translate].names[target_language] = translations_languages[language_to_translate]
                elif translations_languages[language_to_translate] \
                     == langtable._languages_db[language_to_translate].names[target_language]:
                    if opts['debug']:
                        print("Identical: %(language_to_translate)s → %(target_language)s = %(tr)s" %{
                            'language_to_translate': language_to_translate,
                            'target_language': target_language,
                            'tr': translations_languages[language_to_translate]})
                else:
                    print("- %(language_to_translate)s → %(target_language)s = %(tr)s" %{
                        'language_to_translate': language_to_translate,
                        'target_language': target_language,
                        'tr': langtable._languages_db[language_to_translate].names[target_language]})
                    print("+ %(language_to_translate)s → %(target_language)s = %(tr)s" %{
                        'language_to_translate': language_to_translate,
                        'target_language': target_language,
                        'tr': translations_languages[language_to_translate]})
                    if include_changes:
                        langtable._languages_db[language_to_translate].names[target_language] = translations_languages[language_to_translate]
            else:
                if opts['debug']:
                    print("Not in langtable: %(language_to_translate)s" %{
                        'language_to_translate': language_to_translate})
        for territory_to_translate in translations_territories:
            if translations_territories[territory_to_translate] in ('↑↑↑',):
                continue
            if territory_to_translate in langtable._territories_db:
                if target_language not in langtable._territories_db[territory_to_translate].names:
                    print("Missing: %(territory_to_translate)s → %(target_language)s = %(tr)s" %{'territory_to_translate': territory_to_translate,
                                                                                                  'target_language': target_language,
                                                                                                  'tr': translations_territories[territory_to_translate]})
                    langtable._territories_db[territory_to_translate].names[target_language] = translations_territories[territory_to_translate]
                elif translations_territories[territory_to_translate] \
                     == langtable._territories_db[territory_to_translate].names[target_language]:
                    if opts['debug']:
                        print("Identical: %(territory_to_translate)s → %(target_language)s = %(tr)s" %{'territory_to_translate': territory_to_translate,
                                                                                                        'target_language': target_language,
                                                                                                        'tr': translations_territories[territory_to_translate]})
                else:
                    print("- %(territory_to_translate)s → %(target_language)s = %(tr)s" %{
                        'territory_to_translate': territory_to_translate,
                        'target_language': target_language,
                        'tr': langtable._territories_db[territory_to_translate].names[target_language]})
                    print("+ %(territory_to_translate)s → %(target_language)s = %(tr)s" %{'territory_to_translate': territory_to_translate,
                                                                                           'target_language': target_language,
                                                                                           'tr': translations_territories[territory_to_translate]})
                    if include_changes:
                        langtable._territories_db[territory_to_translate].names[target_language] = translations_territories[territory_to_translate]
            else:
                if opts['debug']:
                    print("Not in langtable: %(territory_to_translate)s" %{
                        'territory_to_translate': territory_to_translate})
        for timezone_city_to_translate in translations_timezone_cities:
            if translations_timezone_cities[timezone_city_to_translate] in ('↑↑↑',):
                continue
            if timezone_city_to_translate in langtable._timezoneIdParts_db:
                if target_language not in langtable._timezoneIdParts_db[timezone_city_to_translate].names:
                    if timezone_city_to_translate not in ['Vevay', 'Center']:
                        print("Missing: %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" %{
                            'timezone_city_to_translate': timezone_city_to_translate,
                            'target_language': target_language,
                            'tr': translations_timezone_cities[timezone_city_to_translate]})
                        langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language] = translations_timezone_cities[timezone_city_to_translate]
                elif translations_timezone_cities[timezone_city_to_translate] \
                     == langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language]:
                    if opts['debug']:
                        print("Identical: %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" %{
                            'timezone_city_to_translate': timezone_city_to_translate,
                            'target_language': target_language,
                            'tr': translations_timezone_cities[timezone_city_to_translate]})
                else:
                    if timezone_city_to_translate not in ['Marengo', 'Knox', 'Tell_City', 'Beulah', 'Winamac', 'Vincennes', 'Petersburg', 'Monticello', 'New_Salem', 'Center', 'Melbourne', 'Darwin', 'Hobart', 'Sydney', 'Broken_Hill', 'Mendoza', 'Perth', 'San_Juan', 'Cordoba', 'Brisbane', 'Adelaide', 'Catamarca', 'Currie', 'Vevay', 'Eucla']:
                        print("- %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" %{
                            'timezone_city_to_translate': timezone_city_to_translate,
                            'target_language': target_language,
                            'tr': langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language]})
                        print("+ %(timezone_city_to_translate)s → %(target_language)s = %(tr)s" %{
                            'timezone_city_to_translate': timezone_city_to_translate,
                            'target_language': target_language,
                            'tr': translations_timezone_cities[timezone_city_to_translate]})
                        if include_changes:
                            langtable._timezoneIdParts_db[timezone_city_to_translate].names[target_language] = translations_timezone_cities[timezone_city_to_translate]
    return

def _test_timezone_names():
    from pytz import common_timezones
    languages_supported_by_anaconda = ['af', 'am', 'ar', 'as', 'ast', 'bal', 'be', 'bg', 'bn', 'bn_IN', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'de_CH', 'el', 'en', 'en_GB', 'es', 'et', 'eu', 'eu_ES', 'fa', 'fi', 'fr', 'gl', 'gu', 'he', 'hi', 'hr', 'hu', 'hy', 'ia', 'id', 'ilo', 'is', 'it', 'ja', 'ka', 'kk', 'kn', 'ko', 'lt', 'lv', 'mai', 'mk', 'ml', 'mr', 'ms', 'nb', 'nds', 'ne', 'nl', 'nn', 'nso', 'or', 'pa', 'pl', 'pt', 'pt_BR', 'ro', 'ru', 'si', 'sk', 'sl', 'sq', 'sr', 'sr_Latn', 'sv', 'ta', 'te', 'tg', 'th', 'tr', 'uk', 'ur', 'vi', 'zh_CN', 'zh_TW', 'zu']
    for icuLocaleId in languages_supported_by_anaconda:
        for timezoneId in common_timezones:
            print("%(lang)s: '%(id)s' -> '%(tr)s'" %{
                'lang': icuLocaleId,
                'id': timezoneId,
                'tr': timezone_name(timezoneId=timezoneId, languageIdQuery=icuLocaleId)})
def main():
    args = parse_args()
    if args.debug:
        opts['debug'] = True
    else:
        opts['debug'] = False

    langtable._init(debug = True,
                    logfilename = args.logfilename)

    get_translations_from_cldr(
        main_cldr_dir='/local/mfabian/src/cldr/common/main',
        include_changes=args.include_changes)

    #_test_timezone_names()

    langtable._write_files(territoriesfilename = args.territoriesoutputfile,
                           languagesfilename = args.languagesoutputfile,
                           keyboardsfilename = args.keyboardsoutputfile,
                           timezonesfilename = args.timezonesoutputfile,
                           timezoneidpartsfilename = args.timezoneidpartsoutputfile)

if __name__ == '__main__':
    main()
