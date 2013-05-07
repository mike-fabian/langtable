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

# will be replaced by “make install”:
datadir = '/usr/share/lang-table'

territories = {}
languages = {}
keyboards = {}

class territory:
    def __init__(self, names = None, locales=None, languages=None, keyboards=None, consolefonts=None, timezones=None):
        self.names = names
        self.locales = locales
        self.languages = languages
        self.keyboards = keyboards
        self.consolefonts = consolefonts
        self.timezones = timezones

class language:
    def __init__(self, iso639_1=None, iso639_2_t=None, iso639_2_b=None, names=None, locales=None, territories=None, keyboards=None, consolefonts=None, timezones=None):
        self.iso639_1 = iso639_1
        self.iso639_2_t = iso639_2_t
        self.iso639_2_b = iso639_2_b
        self.names = names
        self.locales = locales
        self.territories = territories
        self.keyboards = keyboards
        self.consolefonts = consolefonts
        self.timezones = timezones

class keyboard:
    def __init__(self, description=None, ascii=True, languages=None, territories = None, comment=None):
        self.description = description
        self.ascii  = ascii
        self.comment = comment
        self.languages = languages
        self.territories = territories

def read_territories_file(file):
    territoriesTree = etree.parse(file).getroot()
    if len(territoriesTree):
        if territoriesTree.tag != 'territories':
            logging.error("Wrong tag: territoriesTree.tag=%s." %territoriesTree.tag)
            exit(1)
        for territoryTree in territoriesTree:
            territoryId = None
            names = {}
            locales = {}
            languages = {}
            keyboards = {}
            consolefonts = {}
            timezones = {}
            for territoryElement in territoryTree:
                if territoryElement.tag == 'territoryId':
                    territoryId = territoryElement.text
                elif territoryElement.tag == 'names' and len(territoryElement):
                    for nameTree in territoryElement:
                        if nameTree.tag == 'name' and len(nameTree):
                            languageId = None
                            name = None
                            for nameElement in nameTree:
                                if nameElement.tag == 'languageId':
                                    languageId = nameElement.text
                                elif nameElement.tag == 'name':
                                    name = nameElement.text
                            if languageId != None and name != None:
                                names[languageId] = name
                elif territoryElement.tag  == 'locales' and len(territoryElement):
                    for localeTree in territoryElement:
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
                elif territoryElement.tag  == 'languages' and len(territoryElement):
                    for languageTree in territoryElement:
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
                elif territoryElement.tag == 'keyboards' and len(territoryElement):
                    for keyboardTree in territoryElement:
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
                elif territoryElement.tag == 'consolefonts' and len(territoryElement):
                    for consolefontTree in territoryElement:
                        if consolefontTree.tag == 'consolefont' and len(consolefontTree):
                            consolefontId = None
                            rank = int(0)
                            for consolefontElement in consolefontTree:
                                if consolefontElement.tag == 'consolefontId':
                                    consolefontId = consolefontElement.text
                                elif consolefontElement.tag == 'rank':
                                    rank = int(consolefontElement.text)
                            if consolefontId != None:
                                consolefonts[consolefontId] = rank
                elif territoryElement.tag == 'timezones' and len(territoryElement):
                    for timezoneTree in territoryElement:
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
            if territoryId != None:
                territories[territoryId] = territory(
                    names = names,
                    locales = locales,
                    languages = languages,
                    keyboards = keyboards,
                    consolefonts = consolefonts,
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
            names = {}
            locales = {}
            territories = {}
            keyboards = {}
            consolefonts = {}
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
                elif languageElement.tag == 'names' and len(languageElement):
                    for nameTree in languageElement:
                        if nameTree.tag == 'name' and len(nameTree):
                            languageIdName = None
                            name = None
                            for nameElement in nameTree:
                                if nameElement.tag == 'languageId':
                                    languageIdName = nameElement.text
                                elif nameElement.tag == 'name':
                                    name = nameElement.text
                            if languageId != None and name != None:
                                names[languageIdName] = name
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
                elif languageElement.tag  == 'territories' and len(languageElement):
                    for  territoryTree in languageElement:
                        if territoryTree.tag == 'territory' and len(territoryTree):
                            territoryId = None
                            rank = int(0)
                            for territoryElement in territoryTree:
                                if territoryElement.tag == 'territoryId':
                                    territoryId = territoryElement.text
                                elif territoryElement.tag == 'rank':
                                    rank = int(territoryElement.text)
                            if territoryId != None:
                                territories[territoryId] = rank
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
                elif languageElement.tag == 'consolefonts' and len(languageElement):
                    for consolefontTree in languageElement:
                        if consolefontTree.tag == 'consolefont' and len(consolefontTree):
                            consolefontId = None
                            rank = int(0)
                            for consolefontElement in consolefontTree:
                                if consolefontElement.tag == 'consolefontId':
                                    consolefontId = consolefontElement.text
                                elif consolefontElement.tag == 'rank':
                                    rank = int(consolefontElement.text)
                            if consolefontId != None:
                                consolefonts[consolefontId] = rank
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
                    names = names,
                    locales = locales,
                    territories = territories,
                    keyboards = keyboards,
                    consolefonts = consolefonts,
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
            territories = {}
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
                elif keyboardElement.tag  == 'territories' and len(keyboardElement):
                    for territoryTree in keyboardElement:
                        if territoryTree.tag == 'territory' and len(territoryTree):
                            languageId = None
                            rank = int(0)
                            for territoryElement in territoryTree:
                                if territoryElement.tag == 'territoryId':
                                    territoryId = territoryElement.text
                                elif territoryElement.tag == 'rank':
                                    rank = int(territoryElement.text)
                            if territoryId != None:
                                territories[territoryId] = rank
            if keyboardId != None:
                keyboards[keyboardId] = keyboard(
                    description = description,
                    ascii = ascii,
                    comment = comment,
                    languages = languages,
                    territories = territories)

def write_territories_file(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<territories>\n')
    for territoryId in sorted(territories):
        file.write('  <territory>\n')
        file.write('    <territoryId>'+territoryId+'</territoryId>\n')
        names = territories[territoryId].names
        file.write('    <names>\n')
        for name in sorted(names):
            file.write(
                '      <name>'
                +'<languageId>'+name+'</languageId>'
                +'<name>'+names[name].encode('UTF-8')+'</name>'
                +'</name>\n')
        file.write('    </names>\n')
        locales = territories[territoryId].locales
        file.write('    <locales>\n')
        for localeId, rank in sorted(locales.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <locale>'
                +'<localeId>'+localeId+'</localeId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</locale>\n')
        file.write('    </locales>\n')
        languages = territories[territoryId].languages
        file.write('    <languages>\n')
        for languageId, rank in sorted(languages.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <language>'
                +'<languageId>'+languageId+'</languageId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</language>\n')
        file.write('    </languages>\n')
        keyboards = territories[territoryId].keyboards
        file.write('    <keyboards>\n')
        for keyboardId, rank in sorted(keyboards.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <keyboard>'
                +'<keyboardId>'+keyboardId+'</keyboardId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</keyboard>\n')
        file.write('    </keyboards>\n')
        consolefonts = territories[territoryId].consolefonts
        file.write('    <consolefonts>\n')
        for consolefontId, rank in sorted(consolefonts.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <consolefont>'
                +'<consolefontId>'+consolefontId+'</consolefontId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</consolefont>\n')
        file.write('    </consolefonts>\n')
        timezones = territories[territoryId].timezones
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
    return

def write_languages_file(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<languages>\n')
    for languageId in sorted(languages):
        file.write('  <language>\n')
        file.write('    <languageId>'+languageId+'</languageId>\n')
        file.write('    <iso639-1>'+str(languages[languageId].iso639_1)+'</iso639-1>\n')
        file.write('    <iso639-2-t>'+str(languages[languageId].iso639_2_t)+'</iso639-2-t>\n')
        file.write('    <iso639-2-b>'+str(languages[languageId].iso639_2_b)+'</iso639-2-b>\n')
        names = languages[languageId].names
        file.write('    <names>\n')
        for name in sorted(names):
            file.write(
                '      <name>'
                +'<languageId>'+name+'</languageId>'
                +'<name>'+names[name].encode('UTF-8')+'</name>'
                +'</name>\n')
        file.write('    </names>\n')
        locales = languages[languageId].locales
        file.write('    <locales>\n')
        for localeId, rank in sorted(locales.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <locale>'
                +'<localeId>'+localeId+'</localeId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</locale>\n')
        file.write('    </locales>\n')
        territories = languages[languageId].territories
        file.write('    <territories>\n')
        for territoryId, rank in sorted(territories.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <territory>'
                +'<territoryId>'+territoryId+'</territoryId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</territory>\n')
        file.write('    </territories>\n')
        keyboards = languages[languageId].keyboards
        file.write('    <keyboards>\n')
        for keyboardId, rank in sorted(keyboards.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <keyboard>'
                +'<keyboardId>'+keyboardId+'</keyboardId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</keyboard>\n')
        file.write('    </keyboards>\n')
        consolefonts = languages[languageId].consolefonts
        file.write('    <consolefonts>\n')
        for consolefontId, rank in sorted(consolefonts.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <consolefont>'
                +'<consolefontId>'+consolefontId+'</consolefontId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</consolefont>\n')
        file.write('    </consolefonts>\n')
        timezones = languages[languageId].timezones
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
            file.write('    <comment>'+keyboards[keyboardId].comment.encode('UTF-8')+'</comment>\n')
        languages = keyboards[keyboardId].languages
        file.write('    <languages>\n')
        for languageId, rank in sorted(languages.items(), key=lambda x: (-1*x[1],x[0])):
            file.write(
                '      <language>'
                +'<languageId>'+languageId+'</languageId>'
                +'<rank>'+str(rank)+'</rank>'
                +'</language>\n')
        file.write('    </languages>\n')
        territories = keyboards[keyboardId].territories
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
    return

def read_files(territoriesfilename, languagesfilename, keyboardsfilename):
    with open(territoriesfilename, 'r') as territoriesfile:
        logging.info("reading territories file=%s" %territoriesfile)
        read_territories_file(territoriesfile)
    with open(languagesfilename, 'r') as languagesfile:
        logging.info("reading languages file=%s" %languagesfile)
        read_languages_file(languagesfile)
    with open(keyboardsfilename, 'r') as keyboardsfile:
        logging.info("reading keyboards file=%s" %keyboardsfile)
        read_keyboards_file(keyboardsfile)

def write_files(territoriesfilename, languagesfilename, keyboardsfilename):
    with open(territoriesfilename, 'w') as territoriesfile:
        logging.info("writing territories file=%s" %territoriesfile)
        write_territories_file(territoriesfile)
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

def territory_name(territoryId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None):
    if territoryId in territories:
        if languageIdQuery and scriptIdQuery and territoryIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
            if icuLocaleIdQuery in territories[territoryId].names:
                return territories[territoryId].names[icuLocaleIdQuery]
        if languageIdQuery and scriptIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
            if icuLocaleIdQuery in territories[territoryId].names:
                return territories[territoryId].names[icuLocaleIdQuery]
        if languageIdQuery and territoryIdQuery:
            icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
            if icuLocaleIdQuery in territories[territoryId].names:
                return territories[territoryId].names[icuLocaleIdQuery]
        if languageIdQuery:
            icuLocaleIdQuery = languageIdQuery
            if icuLocaleIdQuery in territories[territoryId].names:
                return territories[territoryId].names[icuLocaleIdQuery]
    return ''

def language_name(languageId = None, scriptId = None, territoryId = None, languageIdQuery = None, scriptIdQuery = None, territoryIdQuery = None):
    if not languageIdQuery:
        # get the endonym
        languageIdQuery = languageId
        scriptIdQuery = scriptId
        territoryIdQuery = territoryId
    if languageId and scriptId and territoryId:
        icuLocaleId = languageId+'_'+scriptId+'_'+territoryId
        if icuLocaleId in languages:
            if languageIdQuery and scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery and scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
    if languageId and scriptId:
        icuLocaleId = languageId+'_'+scriptId
        if icuLocaleId in languages:
            if languageIdQuery and  scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery and  scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
    if languageId and territoryId:
        icuLocaleId = languageId+'_'+territoryId
        if icuLocaleId in languages:
            if languageIdQuery and  scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery and  scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
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
    if languageId:
        icuLocaleId = languageId
        if icuLocaleId in languages:
            if languageIdQuery and  scriptIdQuery and territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery and  scriptIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+scriptIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if  languageIdQuery and  territoryIdQuery:
                icuLocaleIdQuery = languageIdQuery+'_'+territoryIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
            if languageIdQuery:
                icuLocaleIdQuery = languageIdQuery
                if icuLocaleIdQuery in languages[icuLocaleId].names:
                    return languages[icuLocaleId].names[icuLocaleIdQuery]
    return ''

extra_bonus = 1000000

def list_locales(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    ranked_locales = {}
    skipTerritory = False
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in languages:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in languages:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in languages:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
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
    territory_bonus = 1
    if territoryId in territories and not skipTerritory:
        for locale in territories[territoryId].locales:
            if territories[territoryId].locales[locale] != 0:
                if locale not in ranked_locales:
                    ranked_locales[locale] = territories[territoryId].locales[locale]
                else:
                    ranked_locales[locale] *= territories[territoryId].locales[locale]
                    ranked_locales[locale] *= extra_bonus
                ranked_locales[locale] *= territory_bonus
    ranked_list = dictionary_to_ranked_list(ranked_locales)
    if concise:
        ranked_list = make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    else:
        return ranked_list_to_list(ranked_list)

def list_keyboards(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    ranked_keyboards = {}
    skipTerritory = False
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in languages:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in languages:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in languages:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
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
    territory_bonus = 1
    if territoryId in territories:
        for keyboard in territories[territoryId].keyboards:
            if territories[territoryId].keyboards[keyboard] != 0:
                if keyboard not in ranked_keyboards:
                    ranked_keyboards[keyboard] = territories[territoryId].keyboards[keyboard]
                else:
                    ranked_keyboards[keyboard] *= territories[territoryId].keyboards[keyboard]
                    ranked_keyboards[keyboard] *= extra_bonus
                ranked_keyboards[keyboard] *= territory_bonus
    ranked_list = dictionary_to_ranked_list(ranked_keyboards)
    if concise:
        ranked_list = make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    else:
        return ranked_list_to_list(ranked_list)

def list_consolefonts(concise=True, show_weights=False, languageId = None, scriptId = None, territoryId = None):
    ranked_consolefonts = {}
    skipTerritory = False
    if languageId and scriptId and territoryId and languageId+'_'+scriptId+'_'+territoryId in languages:
        languageId = languageId+'_'+scriptId+'_'+territoryId
        skipTerritory = True
    elif languageId and scriptId and languageId+'_'+scriptId in languages:
        languageId = languageId+'_'+scriptId
    elif languageId and territoryId and languageId+'_'+territoryId in languages:
        languageId = languageId+'_'+territoryId
        skipTerritory = True
    language_bonus = 100
    if languageId in languages:
        for consolefont in languages[languageId].consolefonts:
            if languages[languageId].consolefonts[consolefont] != 0:
                if consolefont not in ranked_consolefonts:
                    ranked_consolefonts[consolefont] = languages[languageId].consolefonts[consolefont]
                else:
                    ranked_consolefonts[consolefont] *= languages[languageId].consolefonts[consolefont]
                    ranked_consolefonts[consolefont] *= extra_bonus
                ranked_consolefonts[consolefont] *= language_bonus
    territory_bonus = 1
    if territoryId in territories:
        for consolefont in territories[territoryId].consolefonts:
            if territories[territoryId].consolefonts[consolefont] != 0:
                if consolefont not in ranked_consolefonts:
                    ranked_consolefonts[consolefont] = territories[territoryId].consolefonts[consolefont]
                else:
                    ranked_consolefonts[consolefont] *= territories[territoryId].consolefonts[consolefont]
                    ranked_consolefonts[consolefont] *= extra_bonus
                ranked_consolefonts[consolefont] *= territory_bonus
    ranked_list = dictionary_to_ranked_list(ranked_consolefonts)
    if concise:
        ranked_list = make_ranked_list_concise(ranked_list)
    if show_weights:
        return ranked_list
    else:
        return ranked_list_to_list(ranked_list)

def test_language_territory(show_weights=False, languageId=None, scriptId=None, territoryId=None):
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
    return

def init(debug = False,
         logfilename = '/dev/null',
         territoriesfilename = datadir +'/territories.xml',
         languagesfilename = datadir + '/languages.xml',
         keyboardsfilename = datadir + '/keyboards.xml'):
    if not territoriesfilename \
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

    read_files(territoriesfilename,
               languagesfilename,
               keyboardsfilename)

