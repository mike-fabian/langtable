#! /usr/bin/python3

import os
import re
import glob
import langtable

GLIBC_SOURCE_DIR = '/local/mfabian/src/glibc'

def replace_glib_codepoints_with_characters(text):
    pattern = re.compile(
        r'.*(?P<codepoint><U[0-9A-F]{4,8}>)')
    while pattern.match(text):
        match = pattern.match(text)
        codepoint = match.group('codepoint')
        text = text.replace(
            codepoint,
            chr(int(codepoint.replace('<U', '').replace('>', ''), 16)))
    return text

for locale_source in sorted(glob.glob(
        os.path.join(GLIBC_SOURCE_DIR, 'localedata/locales', '*'))):
    locale_id = locale_source.split('/')[-1]
    territory_id = ''
    pattern = re.compile(r'.*(?P<territory>[A-Z]{2})')
    match = pattern.match(locale_id)
    if match:
        territory_id = match.group('territory')
    if 'aa_ER@saaho' in locale_id: # copy aa_ER
        continue
    if 'ca_ES@valencia' in locale_id: # copy ca_ES
        continue
    if 'gez_ER@abegede' in locale_id: # copy gez_ER
        continue
    if 'gez_ET@abegede' in locale_id: # copy gez_ET
        continue
    if '@euro' in locale_id:
        continue
    if 'translit' in locale_id:
        continue
    if 'i18n' in locale_id:
        continue
    if 'POSIX' in locale_id:
        continue
    if 'iso14651' in locale_id:
        continue
    if 'cns11643' in locale_id:
        continue
    if 'sr_RS@latin' in locale_id:
        continue
    if 'zh_CN' in locale_id:
        continue
    if 'zh_HK' in locale_id:
        continue
    if 'zh_TW' in locale_id:
        continue
    with open(locale_source, encoding='UTF-8') as file_handle:
        lines = file_handle.readlines()
        language = ''
        lang_name = ''
        territory = ''
        country_name = ''
        tag = ''
        value = ''
        pattern = re.compile(
            r'^(?P<tag>[a-z_]+)\s+"(?P<value>.+)".*')
        for line in lines:
            match = pattern.match(line)
            if match:
                tag = match.group('tag')
                value = match.group('value')
            if tag == 'language':
                language = value
            if tag == 'lang_name':
                lang_name = value
            if tag == 'territory':
                territory = value
            if tag == 'country_name':
                country_name = value
        lang_name = replace_glib_codepoints_with_characters(lang_name)
        language = replace_glib_codepoints_with_characters(language)
        territory = replace_glib_codepoints_with_characters(territory)
        country_name = replace_glib_codepoints_with_characters(country_name)
        langtable_language_english = langtable.language_name(
            languageId=locale_id, languageIdQuery='en')
        langtable_language_endonym = langtable.language_name(
            languageId=locale_id)
        langtable_territory_english = langtable.territory_name(
            territoryId=territory_id, languageIdQuery='en')
        langtable_territory_endonym = langtable.territory_name(
            territoryId=territory_id, languageIdQuery=locale_id)
        langtable_language_english = langtable_language_english.replace(
            ' (' + langtable_territory_english + ')', '').replace(
                ' (Devanagari script)', '').replace(
                    ' (Latin)', '')
        langtable_language_endonym = langtable_language_endonym.replace(
            ' (' + langtable_territory_endonym + ')', '')
        if langtable_language_endonym != lang_name:
            print('locale_id %s' % locale_id)
            print('    glibc    : lang_name=%s' % lang_name)
            print('    langtable: lang_name=%s' % langtable_language_endonym)
            langtable_language_endonym_codes = ''
            for char in langtable_language_endonym:
                langtable_language_endonym_codes += '<U%04X>' % ord(char)
            print('    langtable: codes=%s'
                  % langtable_language_endonym_codes)
        if langtable_language_english != language:
            print('locale_id %s' % locale_id)
            print('    glibc    : language=%s' % language)
            print('    langtable: language=%s' % langtable_language_english)
            langtable_language_english_codes = ''
            for char in langtable_language_english:
                langtable_language_english_codes += '<U%04X>' % ord(char)
            print('    langtable: codes=%s'
                  % langtable_language_english_codes)
        if langtable_territory_endonym != country_name:
            print('locale_id %s' % locale_id)
            print('    glibc    : country_name=%s' %  country_name)
            print('    langtable: country_name=%s' % langtable_territory_endonym)
            langtable_territory_endonym_codes = ''
            for char in langtable_territory_endonym:
                langtable_territory_endonym_codes += '<U%04X>' % ord(char)
            print('    langtable: codes=%s'
                  % langtable_territory_endonym_codes)


