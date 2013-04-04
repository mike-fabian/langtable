# vim:fileencoding=utf-8:sw=4:et

# Copyright (c) 2013 Mike FABIAN <mfabian@redhat.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import logging
from lxml import etree

countries = {}
languages = {}
keyboards = {}

class country:
    def __init__(self, englishName=None, locales=None, languages=None, keyboards=None, timezones=None):
        self.englishName = englishName
        self.locales = locales
        self.languages = languages
        self.keyboards = keyboards
        self.timezones = timezones

class language:
    def __init__(self, iso639_1=None, iso639_2_t=None, iso639_2_b=None, endonym=None, englishName=None, locales=None, countries=None, keyboards=None, timezones=None):
        self.iso639_1 = iso639_1
        self.iso639_2_t = iso639_2_t
        self.iso639_2_b = iso639_2_b
        self.endonym = endonym
        self.englishName = englishName
        self.locales = locales
        self.countries = countries
        self.keyboards = keyboards
        self.timezones = timezones

class keyboard:
    def __init__(self, description=None, ascii=True, languages=None, comment=None):
        self.description = description
        self.ascii  = ascii
        self.comment = comment
        self.languages = languages
                  
def read_countries_file(file):
    countriesTree = etree.parse(file).getroot()
    if len(countriesTree):
        if countriesTree.tag != 'countries':
            logging.error("Wrong tag: countriesTree.tag=%s." %countriesTree.tag)
            exit(1)
        for countryTree in countriesTree:
            countryId = None
            englishName = None
            locales = {}
            languages = {}
            keyboards = {}
            timezones = {}
            for countryElement in countryTree:
                if countryElement.tag == 'countryId':
                    countryId = countryElement.text
                elif countryElement.tag == 'englishName':
                    englishName = countryElement.text
                elif countryElement.tag  == 'locales' and len(countryElement):
                    for localeTree in countryElement:
                        if localeTree.tag == 'locale' and len(localeTree):
                            localeId = None
                            rank = int(0)
                            for localeElement in localeTree:
                                if localeElement.tag == 'localeId':
                                    localeId = localeElement.text
                                elif localeElement.tag == 'rank':
                                    rank = int(localeElement.text)
                            if localeId != None:
                                locales[localeId] = rank
                elif countryElement.tag  == 'languages' and len(countryElement):
                    for languageTree in countryElement:
                        if languageTree.tag == 'language' and len(languageTree):
                            languageId = None
                            rank = int(0)
                            for languageElement in languageTree:
                                if languageElement.tag == 'languageId':
                                    languageId = languageElement.text
                                elif languageElement.tag == 'rank':
                                    rank = int(languageElement.text)
                            if languageId != None:
                                languages[languageId] = rank
                elif countryElement.tag == 'keyboards' and len(countryElement):
                    for keyboardTree in countryElement:
                        if keyboardTree.tag == 'keyboard' and len(keyboardTree):
                            keyboardId = None
                            rank = int(0)
                            for keyboardElement in keyboardTree:
                                if keyboardElement.tag == 'keyboardId':
                                    keyboardId = keyboardElement.text
                                elif keyboardElement.tag == 'rank':
                                    rank = int(keyboardElement.text)
                            if keyboardId != None:
                                keyboards[keyboardId] = rank
                elif countryElement.tag == 'timezones' and len(countryElement):
                    for timezoneTree in countryElement:
                        if timezoneTree.tag == 'timezone' and len(timezoneTree):
                            timezoneId = None
                            rank  = 0
                            for timezoneElement in timezoneTree:
                                if  timezoneElement.tag == 'timezoneId':
                                    timezoneId = timezoneElement.text
                                elif timezoneElement.tag == 'rank':
                                    rank = int(timezoneElement.text)
                            if timezoneId != None:
                                timezones[timezoneId] = rank
            if countryId != None:
                countries[countryId] = country(
                    englishName = englishName,
                    locales = locales,
                    languages = languages,
                    keyboards = keyboards,
                    timezones = timezones)
    return

def read_languages_file(file):
    languagesTree = etree.parse(file).getroot()
    if len(languagesTree):
        if languagesTree.tag != 'languages':
            logging.error("Wrong tag: languagesTree.tag=%s." %languagesTree.tag)
            exit(1)
        for languageTree in languagesTree:
            languageId = None
            iso639_1 = None
            iso639_2_t = None
            iso639_2_b = None
            endonym =  None
            englishName = None
            locales = {}
            countries = {}
            keyboards = {}
            timezones = {}
            for languageElement in  languageTree:
                if  languageElement.tag == 'languageId':
                    languageId = languageElement.text
                elif languageElement.tag == 'iso639-1':
                    iso639_1 = languageElement.text
                elif languageElement.tag == 'iso639-2-t':
                    iso639_2_t = languageElement.text
                elif languageElement.tag == 'iso639-2-b':
                    iso639_2_b = languageElement.text
                elif languageElement.tag == 'endonym':
                    endonym = languageElement.text
                elif languageElement.tag  == 'englishName':
                    englishName  = languageElement.text
                elif languageElement.tag  == 'locales' and len(languageElement):
                    for  localeTree in languageElement:
                        if localeTree.tag == 'locale' and len(localeTree):
                            localeId = None
                            rank = int(0)
                            for localeElement in localeTree:
                                if localeElement.tag == 'localeId':
                                    localeId = localeElement.text
                                elif localeElement.tag == 'rank':
                                    rank = int(localeElement.text)
                            if localeId != None:
                                locales[localeId] = rank
                elif languageElement.tag  == 'countries' and len(languageElement):
                    for  countryTree in languageElement:
                        if countryTree.tag == 'country' and len(countryTree):
                            countryId = None
                            rank = int(0)
                            for countryElement in countryTree:
                                if countryElement.tag == 'countryId':
                                    countryId = countryElement.text
                                elif countryElement.tag == 'rank':
                                    rank = int(countryElement.text)
                            if countryId != None:
                                countries[countryId] = rank
                elif languageElement.tag == 'keyboards' and len(languageElement):
                    for keyboardTree in languageElement:
                        if keyboardTree.tag == 'keyboard' and len(keyboardTree):
                            keyboardId = None
                            rank = int(0)
                            for keyboardElement in keyboardTree:
                                if keyboardElement.tag == 'keyboardId':
                                    keyboardId = keyboardElement.text
                                elif keyboardElement.tag == 'rank':
                                    rank = int(keyboardElement.text)
                            if keyboardId != None:
                                keyboards[keyboardId] = rank
                elif languageElement.tag == 'timezones' and len(languageElement):
                    for timezoneTree in languageElement:
                        if timezoneTree.tag == 'timezone' and len(timezoneTree):
                            timezoneId = None
                            rank  = 0
                            for timezoneElement in timezoneTree:
                                if  timezoneElement.tag == 'timezoneId':
                                    timezoneId = timezoneElement.text
                                elif timezoneElement.tag == 'rank':
                                    rank = int(timezoneElement.text)
                            if timezoneId != None:
                                timezones[timezoneId] = rank
            if languageId != None:
                languages[languageId] = language(
                    iso639_1 = iso639_1,
                    iso639_2_t = iso639_2_t,
                    iso639_2_b = iso639_2_b,
                    endonym = endonym,
                    englishName = englishName,
                    locales = locales,
                    countries = countries,
                    keyboards = keyboards,
                    timezones = timezones)
    return

def read_keyboards_file(file):
    keyboardsTree = etree.parse(file).getroot()
    if len(keyboardsTree):
        if keyboardsTree.tag != 'keyboards':
            logging.error("Wrong tag: keyboardsTree.tag=%s." %keyboardsTree.tag)
            exit(1)
        for keyboardTree in keyboardsTree:
            keyboardId = None
            description = None
            ascii = True
            comment = None
            languages = {}
            for keyboardElement in keyboardTree:
                if keyboardElement.tag == 'keyboardId':
                    keyboardId = keyboardElement.text
                elif keyboardElement.tag == 'description':
                    description = keyboardElement.text
                elif keyboardElement.tag == 'ascii':
                    ascii = (keyboardElement.text.lower() == u'true')
                elif keyboardElement.tag == 'comment':
                    comment = keyboardElement.text
                elif keyboardElement.tag  == 'languages' and len(keyboardElement):
                    for languageTree in keyboardElement:
                        if languageTree.tag == 'language' and len(languageTree):
                            languageId = None
                            rank = int(0)
                            for languageElement in languageTree:
                                if languageElement.tag == 'languageId':
                                    languageId = languageElement.text
                                elif languageElement.tag == 'rank':
                                    rank = int(languageElement.text)
                            if languageId != None:
                                languages[languageId] = rank
            if keyboardId != None:
                keyboards[keyboardId] = keyboard(
                    description = description,
                    ascii = ascii,
                    comment = comment,
                    languages = languages)

def write_countries_file(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<countries>\n')
    for countryId in sorted(countries):
        file.write('  <country>\n')
        file.write('    <countryId>'+countryId+'</countryId>\n')
        file.write('    <englishName>'+countries[countryId].englishName+'</englishName>\n')
        locales = countries[countryId].locales
        file.write('    <locales>\n')
        for locale in sorted(locales, key=locales.get, reverse=True):
            file.write(
                '      <locale>'
                +'<localeId>'+locale+'</localeId>'
                +'<rank>'+str(locales[locale])+'</rank>'
                +'</locale>\n')
        file.write('    </locales>\n')
        languages = countries[countryId].languages
        file.write('    <languages>\n')
        for language in sorted(languages, key=languages.get, reverse=True):
            file.write(
                '      <language>'
                +'<languageId>'+language+'</languageId>'
                +'<rank>'+str(languages[language])+'</rank>'
                +'</language>\n')
        file.write('    </languages>\n')
        keyboards = countries[countryId].keyboards
        file.write('    <keyboards>\n')
        for keyboard in sorted(keyboards, key=keyboards.get, reverse=True):
            file.write(
                '      <keyboard>'
                +'<keyboardId>'+keyboard+'</keyboardId>'
                +'<rank>'+str(keyboards[keyboard])+'</rank>'
                +'</keyboard>\n')
        file.write('    </keyboards>\n')
        timezones = countries[countryId].timezones
        file.write('    <timezones>\n')
        for timezone in sorted(timezones, key=timezones.get, reverse=True):
            file.write(
                '      <timezone>'
                +'<timezoneId>'+timezone+'</timezoneId>'
                +'<rank>'+str(timezones[timezone])+'</rank>'
                +'</timezone>\n')
        file.write('    </timezones>\n')
        file.write('  </country>\n')
    file.write('</countries>\n')
    return

def write_languages_file(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<languages>\n')
    for languageId in sorted(languages):
        file.write('  <language>\n')
        file.write('    <languageId>'+languageId+'</languageId>\n')
        file.write('    <iso639-1>'+languages[languageId].iso639_1+'</iso639-1>\n')
        file.write('    <iso639-2-t>'+languages[languageId].iso639_2_t+'</iso639-2-t>\n')
        file.write('    <iso639-2-b>'+languages[languageId].iso639_2_b+'</iso639-2-b>\n')
        file.write('    <endonym>'+languages[languageId].endonym.encode('UTF-8')+'</endonym>\n')
        file.write('    <englishName>'+languages[languageId].englishName+'</englishName>\n')
        locales = languages[languageId].locales
        file.write('    <locales>\n')
        for locale in sorted(locales, key=locales.get, reverse=True):
            file.write(
                '      <locale>'
                +'<localeId>'+locale+'</localeId>'
                +'<rank>'+str(locales[locale])+'</rank>'
                +'</locale>\n')
        file.write('    </locales>\n')
        countries = languages[languageId].countries
        file.write('    <countries>\n')
        for country in sorted(countries, key=countries.get, reverse=True):
            file.write(
                '      <country>'
                +'<countryId>'+country+'</countryId>'
                +'<rank>'+str(countries[country])+'</rank>'
                +'</country>\n')
        file.write('    </countries>\n')
        keyboards = languages[languageId].keyboards
        file.write('    <keyboards>\n')
        for keyboard in sorted(keyboards, key=keyboards.get, reverse=True):
            file.write(
                '      <keyboard>'
                +'<keyboardId>'+keyboard+'</keyboardId>'
                +'<rank>'+str(keyboards[keyboard])+'</rank>'
                +'</keyboard>\n')
        file.write('    </keyboards>\n')
        timezones = languages[languageId].timezones
        file.write('    <timezones>\n')
        for timezone in sorted(timezones, key=timezones.get, reverse=True):
            file.write(
                '      <timezone>'
                +'<timezoneId>'+timezone+'</timezoneId>'
                +'<rank>'+str(timezones[timezone])+'</rank>'
                +'</timezone>\n')
        file.write('    </timezones>\n')
        file.write('  </language>\n')
    file.write('</languages>\n')
    return

def write_keyboards_file(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<keyboards>\n')
    for keyboardId in sorted(keyboards):
        file.write('  <keyboard>\n')
        file.write('    <keyboardId>'+keyboardId+'</keyboardId>\n')
        file.write('    <description>'+keyboards[keyboardId].description+'</description>\n')
        file.write('    <ascii>'+str(keyboards[keyboardId].ascii)+'</ascii>\n')
        if keyboards[keyboardId].comment != None:
            file.write('    <comment>'+keyboards[keyboardId].comment+'</comment>\n')
        languages = keyboards[keyboardId].languages
        file.write('    <languages>\n')
        for language in sorted(languages, key=languages.get, reverse=True):
            file.write(
                '      <language>'
                +'<languageId>'+language+'</languageId>'
                +'<rank>'+str(languages[language])+'</rank>'
                +'</language>\n')
        file.write('    </languages>\n')
        file.write('  </keyboard>\n')
    file.write('</keyboards>\n')
    return

def read_files(countriesfilename, languagesfilename, keyboardsfilename):
    with open(countriesfilename, 'r') as countriesfile:
        logging.info("reading countries file=%s" %countriesfile)
        read_countries_file(countriesfile)
    with open(languagesfilename, 'r') as languagesfile:
        logging.info("reading languages file=%s" %languagesfile)
        read_languages_file(languagesfile)
    with open(keyboardsfilename, 'r') as keyboardsfile:
        logging.info("reading keyboards file=%s" %keyboardsfile)
        read_keyboards_file(keyboardsfile)

def write_files(countriesfilename, languagesfilename, keyboardsfilename):
    with open(countriesfilename, 'w') as countriesfile:
        logging.info("writing countries file=%s" %countriesfile)
        write_countries_file(countriesfile)
    with open(languagesfilename, 'w') as languagesfile:
        logging.info("writing languages file=%s" %languagesfile)
        write_languages_file(languagesfile)
    with open(keyboardsfilename, 'w') as keyboardsfile:
        logging.info("writing keyboards file=%s" %keyboardsfile)
        write_keyboards_file(keyboardsfile)
    return

def dictionary_to_ranked_list(dict, reverse=True):
    sorted_list = []
    for item in sorted(dict, key=dict.get, reverse=reverse):
        sorted_list.append([item, dict[item]])
    return sorted_list

def ranked_list_to_list(list):
    return map(lambda x: x[0], list)

def make_ranked_list_concise(ranked_list, cut_off_factor=1000):
    if not len(ranked_list) > 1:
        return ranked_list
    for i in range(0,len(ranked_list)-1):
        if ranked_list[i][1]/ranked_list[i+1][1] > cut_off_factor:
            ranked_list = ranked_list[0:i+1]
            break
    return ranked_list

extra_bonus = 1000000
    
def list_locales(concise=True, show_weights=False, languageId = None, countryId = None):
    ranked_locales = {}
    language_bonus = 100
    if languageId in languages:
        for locale in languages[languageId].locales:
            if languages[languageId].locales[locale] != 0:
                if locale not in ranked_locales:
                    ranked_locales[locale] = languages[languageId].locales[locale]
                else:
                    ranked_locales[locale] *= languages[languageId].locales[locale]
                    ranked_locales[locale] *= extra_bonus
                ranked_locales[locale] *= language_bonus
    country_bonus = 1
    if countryId in countries:
        for locale in countries[countryId].locales:
            if countries[countryId].locales[locale] != 0:
                if locale not in ranked_locales:
                    ranked_locales[locale] = countries[countryId].locales[locale]
                else:
                    ranked_locales[locale] *= countries[countryId].locales[locale]
                    ranked_locales[locale] *= extra_bonus
                ranked_locales[locale] *= country_bonus
    ranked_list = dictionary_to_ranked_list(ranked_locales)
    if concise:
        ranked_list = make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    else:
        return ranked_list_to_list(ranked_list)

def list_keyboards(concise=True, show_weights=False, languageId = None, countryId = None):
    ranked_keyboards = {}
    language_bonus = 1
    if languageId in languages:
        for keyboard in languages[languageId].keyboards:
            if languages[languageId].keyboards[keyboard] != 0:
                if keyboard not in ranked_keyboards:
                    ranked_keyboards[keyboard] = languages[languageId].keyboards[keyboard]
                else:
                    ranked_keyboards[keyboard] *= languages[languageId].keyboards[keyboard]
                    ranked_keyboards[keyboard] *= extra_bonus
                ranked_keyboards[keyboard] *= language_bonus
    country_bonus = 1
    if countryId in countries:
        for keyboard in countries[countryId].keyboards:
            if countries[countryId].keyboards[keyboard] != 0:
                if keyboard not in ranked_keyboards:
                    ranked_keyboards[keyboard] = countries[countryId].keyboards[keyboard]
                else:
                    ranked_keyboards[keyboard] *= countries[countryId].keyboards[keyboard]
                    ranked_keyboards[keyboard] *= extra_bonus
                ranked_keyboards[keyboard] *= country_bonus
    ranked_list = dictionary_to_ranked_list(ranked_keyboards)
    if concise:
        ranked_list = make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    else:
        return ranked_list_to_list(ranked_list)

def test_language_country(show_weights=False, languageId=None, countryId=None):
    print(str(languageId)+": "
          +repr(list_locales(show_weights=show_weights,languageId=languageId))
          +'\n'
          +str(countryId)+": "
          +repr(list_locales(show_weights=show_weights,countryId=countryId))
          +'\n'
          +" +: "
          +repr(list_locales(show_weights=show_weights,languageId=languageId,countryId=countryId))
          +'\n'
          +str(languageId)+": "
          +repr(list_keyboards(show_weights=show_weights,languageId=languageId))
          +'\n'
          +str(countryId)+": "
          +repr(list_keyboards(show_weights=show_weights,countryId=countryId))
          +'\n'
          +" +: "
          +repr(list_keyboards(show_weights=show_weights,languageId=languageId,countryId=countryId))
          )
    return

def init(debug = False,
         logfilename = '/dev/null',
         countriesfilename = None,
         languagesfilename = None,
         keyboardsfilename = None):
    if not countriesfilename \
       or not languagesfilename \
       or not keyboardsfilename:
        return
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(filename=logfilename,
                        filemode="w",
                        format="%(levelname)s: %(message)s",
                        level=log_level)

    read_files(countriesfilename,
               languagesfilename,
               keyboardsfilename)

    write_files(countriesfilename+'.new',
                languagesfilename+'.new',
                keyboardsfilename+'.new')

