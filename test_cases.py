# vim:fileencoding=utf-8:sw=4:et -*- coding: utf-8 -*-

import sys

def dummy():
    u'''
    >>> import langtable
    >>> from langtable import list_locales
    >>> from langtable import list_scripts
    >>> from langtable import list_keyboards
    >>> from langtable import list_inputmethods
    >>> from langtable import list_consolefonts
    >>> from langtable import _test_language_territory
    >>> from langtable import language_name
    >>> from langtable import territory_name
    >>> from langtable import _test_cldr_locale_pattern
    >>> from langtable import supports_ascii
    >>> from langtable import languageId

    ######################################################################
    # Start of tests to reproduce the results from mangleLocale(inLocale) in anaconda, see:
    # https://git.fedorahosted.org/cgit/anaconda.git/tree/pyanaconda/localization.py#n121

    >>> list_locales(show_weights=False, languageId="af") # doctest: +NORMALIZE_WHITESPACE
        ['af_ZA.UTF-8']

    >>> list_locales(show_weights=False, languageId="am") # doctest: +NORMALIZE_WHITESPACE
        ['am_ET.UTF-8']

    # this puts ar_EG first instead of ar_SA from mangleLocale
    # (because EG is the Arabic country with the most inhabitants).
    # But this should not matter, all our Arabic translations
    # are in /usr/share/locale/ar/LC_MESSAGES/ at the moment, i.e. we do
    # not have different Arabic translations for different territories anyway,
    # than it does not matter that much which Arabic locale is choosen.
    # So I do not need to tweak the weights  here, I think.
    >>> list_locales(show_weights=False, languageId="ar") # doctest: +NORMALIZE_WHITESPACE
        ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']

    >>> list_locales(show_weights=False, languageId="as") # doctest: +NORMALIZE_WHITESPACE
        ['as_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="ast") # doctest: +NORMALIZE_WHITESPACE
        ['ast_ES.UTF-8']

    >>> list_locales(show_weights=False, languageId="be") # doctest: +NORMALIZE_WHITESPACE
        ['be_BY.UTF-8', 'be_BY.UTF-8@latin']

    >>> list_locales(show_weights=False, languageId="bg") # doctest: +NORMALIZE_WHITESPACE
        ['bg_BG.UTF-8']

    >>> list_locales(show_weights=False, languageId="bn") # doctest: +NORMALIZE_WHITESPACE
        ['bn_BD.UTF-8', 'bn_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="bs") # doctest: +NORMALIZE_WHITESPACE
        ['bs_BA.UTF-8']

    >>> list_locales(show_weights=False, languageId="ca") # doctest: +NORMALIZE_WHITESPACE
        ['ca_ES.UTF-8', 'ca_ES.UTF-8@valencia', 'ca_FR.UTF-8', 'ca_AD.UTF-8', 'ca_IT.UTF-8']

    >>> list_locales(show_weights=False, languageId="ca_ES_VALENCIA") # doctest: +NORMALIZE_WHITESPACE
        ['ca_ES.UTF-8@valencia']

    >>> list_locales(show_weights=False, languageId="ca_ES_VALENCIA", territoryId='ES') # doctest: +NORMALIZE_WHITESPACE
        ['ca_ES.UTF-8@valencia']

    >>> list_locales(show_weights=False, languageId="cs") # doctest: +NORMALIZE_WHITESPACE
        ['cs_CZ.UTF-8']

    >>> list_locales(show_weights=False, languageId="cy") # doctest: +NORMALIZE_WHITESPACE
        ['cy_GB.UTF-8']

    >>> list_locales(show_weights=False, languageId="da") # doctest: +NORMALIZE_WHITESPACE
        ['da_DK.UTF-8']

    >>> list_locales(show_weights=False, languageId="de") # doctest: +NORMALIZE_WHITESPACE
        ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']

    >>> list_locales(show_weights=False, languageId="el") # doctest: +NORMALIZE_WHITESPACE
        ['el_GR.UTF-8', 'el_CY.UTF-8']

    >>> list_locales(show_weights=False, languageId="eo") # doctest: +NORMALIZE_WHITESPACE
        ['eo.UTF-8']

    >>> list_locales(show_weights=False, languageId="en") # doctest: +NORMALIZE_WHITESPACE
        ['en_US.UTF-8', 'en_GB.UTF-8', 'en_IN.UTF-8', 'en_AU.UTF-8', 'en_CA.UTF-8', 'en_DK.UTF-8', 'en_IE.UTF-8', 'en_NZ.UTF-8', 'en_NG.UTF-8', 'en_HK.UTF-8', 'en_PH.UTF-8', 'en_SG.UTF-8', 'en_ZA.UTF-8', 'en_ZM.UTF-8', 'en_ZW.UTF-8', 'en_BW.UTF-8', 'en_AG.UTF-8', 'en_IL.UTF-8']

    # I put es_ES first here which is kind of arbitrary, Spain isn’t the
    # country with the biggest number of Spanish speaking people, but that
    # is what Anaconda’s mangleMap did so far and it is not clear which
    # country to put first in that list anyway.
    >>> list_locales(show_weights=False, languageId="es") # doctest: +NORMALIZE_WHITESPACE
        ['es_ES.UTF-8', 'es_VE.UTF-8', 'es_UY.UTF-8', 'es_US.UTF-8', 'es_SV.UTF-8', 'es_PY.UTF-8', 'es_PR.UTF-8', 'es_PE.UTF-8', 'es_PA.UTF-8', 'es_NI.UTF-8', 'es_MX.UTF-8', 'es_HN.UTF-8', 'es_GT.UTF-8', 'es_EC.UTF-8', 'es_DO.UTF-8', 'es_CU.UTF-8', 'es_CR.UTF-8', 'es_CO.UTF-8', 'es_CL.UTF-8', 'es_BO.UTF-8', 'es_AR.UTF-8']

    >>> list_locales(show_weights=False, languageId="et") # doctest: +NORMALIZE_WHITESPACE
        ['et_EE.UTF-8']

    >>> list_locales(show_weights=False, languageId="eu") # doctest: +NORMALIZE_WHITESPACE
        ['eu_ES.UTF-8']

    >>> list_locales(show_weights=False, languageId="fa") # doctest: +NORMALIZE_WHITESPACE
        ['fa_IR.UTF-8']

    >>> list_locales(show_weights=False, languageId="fi") # doctest: +NORMALIZE_WHITESPACE
        ['fi_FI.UTF-8']

    >>> list_locales(show_weights=False, languageId="fr") # doctest: +NORMALIZE_WHITESPACE
        ['fr_FR.UTF-8', 'fr_CA.UTF-8', 'fr_BE.UTF-8', 'fr_CH.UTF-8', 'fr_LU.UTF-8']

    >>> list_locales(show_weights=False, languageId="gl") # doctest: +NORMALIZE_WHITESPACE
        ['gl_ES.UTF-8']

    >>> list_locales(show_weights=False, languageId="gu") # doctest: +NORMALIZE_WHITESPACE
        ['gu_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="he") # doctest: +NORMALIZE_WHITESPACE
        ['he_IL.UTF-8']

    >>> list_locales(show_weights=False, languageId="hi") # doctest: +NORMALIZE_WHITESPACE
        ['hi_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="hr") # doctest: +NORMALIZE_WHITESPACE
        ['hr_HR.UTF-8']

    >>> list_locales(show_weights=False, languageId="hu") # doctest: +NORMALIZE_WHITESPACE
        ['hu_HU.UTF-8']

    >>> list_locales(show_weights=False, languageId="hy") # doctest: +NORMALIZE_WHITESPACE
        ['hy_AM.UTF-8']

    >>> list_locales(show_weights=False, languageId="id") # doctest: +NORMALIZE_WHITESPACE
        ['id_ID.UTF-8']

    # we have no ilo_PH.UTF-8 locale in glibc!
    >>> list_locales(show_weights=False, languageId="ilo") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_locales(show_weights=False, languageId="is") # doctest: +NORMALIZE_WHITESPACE
        ['is_IS.UTF-8']

    >>> list_locales(show_weights=False, languageId="it") # doctest: +NORMALIZE_WHITESPACE
        ['it_IT.UTF-8', 'it_CH.UTF-8']

    >>> list_locales(show_weights=False, languageId="ja") # doctest: +NORMALIZE_WHITESPACE
        ['ja_JP.UTF-8']

    >>> list_locales(show_weights=False, languageId="ka") # doctest: +NORMALIZE_WHITESPACE
        ['ka_GE.UTF-8']

    >>> list_locales(show_weights=False, languageId="kk") # doctest: +NORMALIZE_WHITESPACE
        ['kk_KZ.UTF-8']

    >>> list_locales(show_weights=False, languageId="kn") # doctest: +NORMALIZE_WHITESPACE
        ['kn_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="ko") # doctest: +NORMALIZE_WHITESPACE
        ['ko_KR.UTF-8']

    >>> list_locales(show_weights=False, languageId="lt") # doctest: +NORMALIZE_WHITESPACE
        ['lt_LT.UTF-8']

    >>> list_locales(show_weights=False, languageId="lv") # doctest: +NORMALIZE_WHITESPACE
        ['lv_LV.UTF-8']

    >>> list_locales(show_weights=False, languageId="mai") # doctest: +NORMALIZE_WHITESPACE
        ['mai_IN.UTF-8', 'mai_NP.UTF-8']

    >>> list_locales(show_weights=False, languageId="mk") # doctest: +NORMALIZE_WHITESPACE
        ['mk_MK.UTF-8']

    >>> list_locales(show_weights=False, languageId="ml") # doctest: +NORMALIZE_WHITESPACE
        ['ml_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="mr") # doctest: +NORMALIZE_WHITESPACE
        ['mr_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="ms") # doctest: +NORMALIZE_WHITESPACE
        ['ms_MY.UTF-8']

    >>> list_locales(show_weights=False, languageId="nb") # doctest: +NORMALIZE_WHITESPACE
        ['nb_NO.UTF-8']

    # this puts nds_NL first instead of nds_DE from mangleLocale
    # (because there seem to be more speakers of nds in NL than in DE).
    # It should not matter at though at the moment, all our nds translations
    # are  in /usr/share/locale/nds/LC_MESSAGES/ at the moment,
    # the right translations will be chosen no matter whether nds_DE.UTF-8
    # or nds_NL.UTF-8 is set as the locale.
    >>> list_locales(show_weights=False, languageId="nds") # doctest: +NORMALIZE_WHITESPACE
        ['nds_NL.UTF-8', 'nds_DE.UTF-8']

    >>> list_locales(show_weights=False, languageId="ne") # doctest: +NORMALIZE_WHITESPACE
        ['ne_NP.UTF-8']

    >>> list_locales(show_weights=False, languageId="nl") # doctest: +NORMALIZE_WHITESPACE
        ['nl_NL.UTF-8', 'nl_BE.UTF-8', 'nl_AW.UTF-8']

    >>> list_locales(show_weights=False, languageId="nn") # doctest: +NORMALIZE_WHITESPACE
        ['nn_NO.UTF-8']

    >>> list_locales(show_weights=False, languageId="nso") # doctest: +NORMALIZE_WHITESPACE
        ['nso_ZA.UTF-8']

    >>> list_locales(show_weights=False, languageId="or") # doctest: +NORMALIZE_WHITESPACE
        ['or_IN.UTF-8']

    # This puts pa_IN first instead of pa_PK to make it do the
    # same as mangleLocale did. There seem to be more speakers of pa in PK
    # than in IN, nevertheless pa_IN is more important for us because
    # we have *only* Punjabi translations for India (all our Punjabi
    # translations use Gurmukhi script (used by the pa_IN.UTF-8 glibc locale).
    # None of our translations use the Perso-Arabic Shahmukhī alphabet
    # used by the pa_PK.UTF-8 glibc locale.
    # All of our Punjabi translations are currently in /usr/share/locale/pa,
    # as they use the Gurmukhi script and seem to be specific to India,
    # they should probably move to /usr/share/locale/pa_IN in future.
    #
    # Giving pa_IN.UTF-8 higher weight should fix
    # https://bugzilla.redhat.com/show_bug.cgi?id=986155
    # Bug 986155 - Punjabi (India) missing in language installation list
    >>> list_locales(show_weights=False, languageId="pa") # doctest: +NORMALIZE_WHITESPACE
        ['pa_IN.UTF-8', 'pa_PK.UTF-8']

    >>> list_locales(show_weights=False, languageId="pl") # doctest: +NORMALIZE_WHITESPACE
        ['pl_PL.UTF-8']

    # different from mangleLocale which gives pt_PT
    # (because Brazil is much bigger than Portugal).
    # Anaconda has translations for both Brasilian and Portuguese Portuguese:
    # $ ls /usr/share/locale/pt*/LC_MESSAGES/*anaco*
    # /usr/share/locale/pt/LC_MESSAGES/anaconda.mo
    # /usr/share/locale/pt_BR/LC_MESSAGES/anaconda.mo
    # So Anaconda needs to be specific here, just selecting languageId="pt"
    # cannot be enough.
    >>> list_locales(show_weights=False, languageId="pt") # doctest: +NORMALIZE_WHITESPACE
        ['pt_BR.UTF-8', 'pt_PT.UTF-8']

    >>> list_locales(show_weights=False, languageId="ro") # doctest: +NORMALIZE_WHITESPACE
        ['ro_RO.UTF-8']

    >>> list_locales(show_weights=False, languageId="ru") # doctest: +NORMALIZE_WHITESPACE
        ['ru_RU.UTF-8', 'ru_UA.UTF-8']

    >>> list_locales(show_weights=False, languageId="si") # doctest: +NORMALIZE_WHITESPACE
        ['si_LK.UTF-8']

    >>> list_locales(show_weights=False, languageId="sk") # doctest: +NORMALIZE_WHITESPACE
        ['sk_SK.UTF-8']

    >>> list_locales(show_weights=False, languageId="sl") # doctest: +NORMALIZE_WHITESPACE
        ['sl_SI.UTF-8']

    >>> list_locales(show_weights=False, languageId="sq") # doctest: +NORMALIZE_WHITESPACE
        ['sq_AL.UTF-8', 'sq_MK.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_RS.UTF-8@latin', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr", scriptId="Cyrl") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr", scriptId="cyrillic") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr", scriptId="Latn") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    >>> list_locales(show_weights=False, languageId="sr", scriptId="latin") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    # the script can also be specified in the languageId.
    # If the script is specified in the languageId already, it takes
    # precedence over a script specified in scriptId:
    >>> list_locales(show_weights=False, languageId="sr_Latn") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    >>> list_locales(show_weights=False, languageId="sr_Latn", scriptId="Latn") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    >>> list_locales(show_weights=False, languageId="sr_Latn", scriptId="Cyrl") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    >>> list_locales(show_weights=False, languageId="sr_Cyrl") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr_cyrillic") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr_Cyrl", scriptId="Latn") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr_cyrillic", scriptId="latin") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sr_latin", scriptId="cyrillic") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    >>> list_locales(show_weights=False, languageId="sr_Cyrl", scriptId="Cyrl") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_ME.UTF-8']

    >>> list_locales(show_weights=False, languageId="sv") # doctest: +NORMALIZE_WHITESPACE
        ['sv_SE.UTF-8', 'sv_FI.UTF-8']

    >>> list_locales(show_weights=False, languageId="ta") # doctest: +NORMALIZE_WHITESPACE
        ['ta_IN.UTF-8', 'ta_LK.UTF-8']

    >>> list_locales(show_weights=False, languageId="te") # doctest: +NORMALIZE_WHITESPACE
        ['te_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="tg") # doctest: +NORMALIZE_WHITESPACE
        ['tg_TJ.UTF-8']

    >>> list_locales(show_weights=False, languageId="th") # doctest: +NORMALIZE_WHITESPACE
        ['th_TH.UTF-8']

    >>> list_locales(show_weights=False, languageId="tr") # doctest: +NORMALIZE_WHITESPACE
        ['tr_TR.UTF-8', 'tr_CY.UTF-8']

    >>> list_locales(show_weights=False, languageId="uk") # doctest: +NORMALIZE_WHITESPACE
        ['uk_UA.UTF-8']

    >>> list_locales(show_weights=False, languageId="ur") # doctest: +NORMALIZE_WHITESPACE
        ['ur_PK.UTF-8', 'ur_IN.UTF-8']

    >>> list_locales(show_weights=False, languageId="vi") # doctest: +NORMALIZE_WHITESPACE
        ['vi_VN.UTF-8']

    >>> list_locales(show_weights=False, languageId="zu") # doctest: +NORMALIZE_WHITESPACE
        ['zu_ZA.UTF-8']

    # End of tests to reproduce the results from mangleLocale(inLocale) in anaconda
    ######################################################################

    >>> list_locales(languageId="de", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['de_BE.UTF-8']

    # territory given in languageId overrides territory given in territoryId:
    >>> list_locales(languageId="sr_RS", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8', 'sr_RS.UTF-8@latin']

    # script given in languageId overrides script given in scriptId:
    >>> list_locales(languageId="sr_Cyrl_RS", scriptId="Latn") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8']

    # script given in languageId overrides script given in scriptId:
    >>> list_locales(languageId="sr_Latn_RS", scriptId="Cyrl") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8@latin']

    # script and territory given in languageId override script and territory in extra parameters:
    >>> list_locales(languageId="sr_Cyrl_RS", scriptId="Latn", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ['sr_RS.UTF-8']

    # if languageId contains an invalid locale id, it is completely ignored:
    >>> list_locales(languageId="sr_CYrl_RS", scriptId="Latn", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ['de_DE.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']

    # Japanese uses a mixture of hiragana, katakana, and kanji:
    >>> list_scripts(languageId='ja') # doctest: +NORMALIZE_WHITESPACE
    ['Hani', 'Hira', 'Kana']

    >>> list_scripts(languageId='ko') # doctest: +NORMALIZE_WHITESPACE
    ['Hang', 'Hani']

    >>> list_scripts(languageId='vi') # doctest: +NORMALIZE_WHITESPACE
    ['Latn', 'Hani']

    >>> list_scripts(languageId='sr') # doctest: +NORMALIZE_WHITESPACE
    ['Cyrl', 'Latn']

    >>> list_scripts(languageId='ks') # doctest: +NORMALIZE_WHITESPACE
    ['Arab', 'Deva']

    >>> list_scripts(languageId='ks', territoryId='IN') # doctest: +NORMALIZE_WHITESPACE
    ['Deva', 'Arab']

    >>> list_scripts(languageId='ks', territoryId='PK') # doctest: +NORMALIZE_WHITESPACE
    ['Arab']

    >>> list_scripts(languageId='ks_PK') # doctest: +NORMALIZE_WHITESPACE
    ['Arab']

    >>> list_scripts(languageId='ks_IN') # doctest: +NORMALIZE_WHITESPACE
    ['Deva', 'Arab']

    >>> list_scripts(languageId='ks_Deva_IN') # doctest: +NORMALIZE_WHITESPACE
    ['Deva']

    >>> list_scripts(languageId='ks_devanagari_IN') # doctest: +NORMALIZE_WHITESPACE
    ['Deva']

    >>> list_scripts(languageId='ks_IN@devanagari') # doctest: +NORMALIZE_WHITESPACE
    ['Deva']

    >>> list_scripts(languageId='ks_Arab_IN@devanagari') # doctest: +NORMALIZE_WHITESPACE
    ['Arab']

    >>> list_scripts(languageId='ks_IN.UTF-8') # doctest: +NORMALIZE_WHITESPACE
    ['Deva', 'Arab']

    >>> list_scripts(languageId='ks_IN.UTF-8@devanagari') # doctest: +NORMALIZE_WHITESPACE
    ['Deva']

    >>> list_scripts(languageId='ks_Arab_IN.UTF-8@devanagari') # doctest: +NORMALIZE_WHITESPACE
    ['Arab']

    >>> list_scripts(languageId='ks_Arab_IN.UTF-8@devanagari', scriptId='Latn') # doctest: +NORMALIZE_WHITESPACE
    ['Arab']

    >>> list_scripts(languageId='de') # doctest: +NORMALIZE_WHITESPACE
    ['Latn']

    >>> list_scripts(languageId='de', scriptId='Cyrl') # doctest: +NORMALIZE_WHITESPACE
    ['Cyrl']

    >>> list_scripts(languageId='de_Cyrl', scriptId='Latn') # doctest: +NORMALIZE_WHITESPACE
    ['Cyrl']

    >>> list_scripts(scriptId='Zzzz') # doctest: +NORMALIZE_WHITESPACE
    ['Zzzz']

    >>> list_keyboards(languageId="de", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['be(oss)']

    # script and territory given in languageId override script and territory in extra parameters:
    >>> list_keyboards(languageId="sr_Latn", scriptId="Cyrl", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['rs(latin)', 'be(oss)']

    # script and territory given in languageId override script and territory in extra parameters:
    >>> list_keyboards(languageId="sr_Latn_RS", scriptId="Cyrl", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['rs(latin)']

    # script and territory given in languageId override script and territory in extra parameters:
    >>> list_keyboards(languageId="sr_Cyrl", scriptId="Latn", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['rs', 'be(oss)']

    # script and territory given in languageId override script and territory in extra parameters:
    >>> list_keyboards(languageId="sr_Cyrl_RS", scriptId="Latn", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        ['rs']

    >>> list_inputmethods(languageId="ja") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/kkc', 'ibus/anthy']

    >>> list_inputmethods(languageId="ja", territoryId="JP") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/kkc', 'ibus/anthy']

    >>> list_inputmethods(languageId="ja", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/kkc', 'ibus/anthy']

    >>> list_inputmethods(languageId="de", territoryId="JP") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/kkc', 'ibus/anthy']

    >>> list_inputmethods(languageId="ko") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/hangul']

    >>> list_inputmethods(languageId="zh") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/libpinyin', 'ibus/libzhuyin', 'ibus/chewing', 'ibus/cangjie']

    >>> list_inputmethods(languageId="zh", territoryId="CN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/libpinyin']

    >>> list_inputmethods(languageId="zh_CN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/libpinyin']

    >>> list_inputmethods(languageId="zh", territoryId="HK") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/cangjie']

    >>> list_inputmethods(languageId="zh", territoryId="MO") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/cangjie']

    >>> list_inputmethods(languageId="zh", territoryId="TW") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/libzhuyin', 'ibus/chewing']

    >>> list_inputmethods(languageId="zh", territoryId="SG") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/libpinyin']

    >>> list_inputmethods(languageId="as", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:as:phonetic']

    >>> list_inputmethods(languageId="as", territoryId="BD") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:as:phonetic']

    >>> list_inputmethods(languageId="bn") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:bn:inscript']

    >>> list_inputmethods(languageId="gu") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:gu:inscript']

    >>> list_inputmethods(languageId="hi") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:hi:inscript']

    >>> list_inputmethods(languageId="kn") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:kn:kgp']

    >>> list_inputmethods(languageId="mai") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:mai:inscript']

    >>> list_inputmethods(languageId="ml") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:ml:inscript']

    >>> list_inputmethods(languageId="mr") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:mr:inscript']

    >>> list_inputmethods(languageId="or") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:or:inscript']

    >>> list_inputmethods(languageId="pa") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:pa:inscript']

    >>> list_inputmethods(languageId="ta") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:ta:tamil99']

    >>> list_inputmethods(languageId="te") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:te:inscript']

    >>> list_inputmethods(languageId="ur") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:ur:phonetic']

    >>> list_inputmethods(languageId="sd") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript']

    >>> list_inputmethods(languageId="sd", scriptId="Deva") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript']

    >>> list_inputmethods(languageId="sd", scriptId="Arab") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_inputmethods(languageId="sd", scriptId="Deva", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript']

    >>> list_inputmethods(languageId="sd", scriptId="Arab", territoryId="PK") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_inputmethods(languageId="sd", scriptId="Deva", territoryId="PK") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript']

    >>> list_inputmethods(languageId="sd", scriptId="Arab", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_inputmethods(languageId="sd", territoryId="PK") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript']

    >>> list_inputmethods(languageId="sd", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript']

    >>> list_consolefonts(languageId="de", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr']

    >>> list_consolefonts(languageId="el") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr', 'iso07u-16', 'LatGrkCyr-8x16']

    >>> list_consolefonts(territoryId="GR") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr', 'iso07u-16', 'LatGrkCyr-8x16']

    >>> list_consolefonts(languageId="el", territoryId="GR") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr']

    >>> list_consolefonts(languageId="el", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr']

    # script and territory given in languageId override script and territory in extra parameters:
    >>> list_consolefonts(languageId="el_GR", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr']

    >>> list_consolefonts(languageId="de", territoryId="GR") # doctest: +NORMALIZE_WHITESPACE
        ['eurlatgr']

    >>> _test_language_territory(show_weights=False, languageId=None, territoryId=None) # doctest: +NORMALIZE_WHITESPACE
        None: []
        None: []
         +: []
        None: []
        None: []
         +: []

    >>> _test_language_territory(show_weights=False, languageId="af", territoryId="ZA") # doctest: +NORMALIZE_WHITESPACE
        af: ['af_ZA.UTF-8']
        ZA: ['zu_ZA.UTF-8', 'xh_ZA.UTF-8', 'af_ZA.UTF-8', 'en_ZA.UTF-8', 'nso_ZA.UTF-8', 'tn_ZA.UTF-8', 'st_ZA.UTF-8', 'ts_ZA.UTF-8', 'ss_ZA.UTF-8', 've_ZA.UTF-8', 'nr_ZA.UTF-8']
         +: ['af_ZA.UTF-8']
        af: ['us(intl)']
        ZA: ['us(intl)', 'us', 'za']
         +: ['us(intl)']

    >>> _test_language_territory(show_weights=False, languageId="nso", territoryId="ZA") # doctest: +NORMALIZE_WHITESPACE
       nso: ['nso_ZA.UTF-8']
        ZA: ['zu_ZA.UTF-8', 'xh_ZA.UTF-8', 'af_ZA.UTF-8', 'en_ZA.UTF-8', 'nso_ZA.UTF-8', 'tn_ZA.UTF-8', 'st_ZA.UTF-8', 'ts_ZA.UTF-8', 'ss_ZA.UTF-8', 've_ZA.UTF-8', 'nr_ZA.UTF-8']
         +: ['nso_ZA.UTF-8']
       nso: ['za']
        ZA: ['us(intl)', 'us', 'za']
         +: ['za']

    >>> _test_language_territory(show_weights=False, languageId="tn", territoryId="ZA") # doctest: +NORMALIZE_WHITESPACE
        tn: ['tn_ZA.UTF-8']
        ZA: ['zu_ZA.UTF-8', 'xh_ZA.UTF-8', 'af_ZA.UTF-8', 'en_ZA.UTF-8', 'nso_ZA.UTF-8', 'tn_ZA.UTF-8', 'st_ZA.UTF-8', 'ts_ZA.UTF-8', 'ss_ZA.UTF-8', 've_ZA.UTF-8', 'nr_ZA.UTF-8']
         +: ['tn_ZA.UTF-8']
        tn: ['za']
        ZA: ['us(intl)', 'us', 'za']
         +: ['za']

    >>> _test_language_territory(show_weights=False, languageId="ve", territoryId="ZA") # doctest: +NORMALIZE_WHITESPACE
        ve: ['ve_ZA.UTF-8']
        ZA: ['zu_ZA.UTF-8', 'xh_ZA.UTF-8', 'af_ZA.UTF-8', 'en_ZA.UTF-8', 'nso_ZA.UTF-8', 'tn_ZA.UTF-8', 'st_ZA.UTF-8', 'ts_ZA.UTF-8', 'ss_ZA.UTF-8', 've_ZA.UTF-8', 'nr_ZA.UTF-8']
         +: ['ve_ZA.UTF-8']
        ve: ['za']
        ZA: ['us(intl)', 'us', 'za']
         +: ['za']

    >>> _test_language_territory(show_weights=False, languageId="be", territoryId="BY") # doctest: +NORMALIZE_WHITESPACE
        be: ['be_BY.UTF-8', 'be_BY.UTF-8@latin']
        BY: ['be_BY.UTF-8', 'be_BY.UTF-8@latin']
         +: ['be_BY.UTF-8']
        be: ['by']
        BY: ['by']
         +: ['by']

    >>> _test_language_territory(show_weights=False, languageId="de", territoryId="CH") # doctest: +NORMALIZE_WHITESPACE
        de: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        CH: ['de_CH.UTF-8', 'fr_CH.UTF-8', 'it_CH.UTF-8', 'wae_CH.UTF-8']
         +: ['de_CH.UTF-8']
        de: ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']
        CH: ['ch', 'ch(fr)', 'it']
         +: ['ch']

    >>> _test_language_territory(show_weights=False, languageId="fr", territoryId="CH") # doctest: +NORMALIZE_WHITESPACE
        fr: ['fr_FR.UTF-8', 'fr_CA.UTF-8', 'fr_BE.UTF-8', 'fr_CH.UTF-8', 'fr_LU.UTF-8']
        CH: ['de_CH.UTF-8', 'fr_CH.UTF-8', 'it_CH.UTF-8', 'wae_CH.UTF-8']
         +: ['fr_CH.UTF-8']
        fr: ['fr(oss)', 'ca', 'ch(fr)']
        CH: ['ch', 'ch(fr)', 'it']
         +: ['ch(fr)']

    >>> _test_language_territory(show_weights=False, languageId="fr", territoryId="FR") # doctest: +NORMALIZE_WHITESPACE
        fr: ['fr_FR.UTF-8', 'fr_CA.UTF-8', 'fr_BE.UTF-8', 'fr_CH.UTF-8', 'fr_LU.UTF-8']
        FR: ['fr_FR.UTF-8', 'br_FR.UTF-8', 'oc_FR.UTF-8', 'ca_FR.UTF-8']
         +: ['fr_FR.UTF-8']
        fr: ['fr(oss)', 'ca', 'ch(fr)']
        FR: ['fr(oss)']
         +: ['fr(oss)']

    >>> _test_language_territory(show_weights=False, languageId="de", territoryId="FR") # doctest: +NORMALIZE_WHITESPACE
        de: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        FR: ['fr_FR.UTF-8', 'br_FR.UTF-8', 'oc_FR.UTF-8', 'ca_FR.UTF-8']
         +: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'fr_FR.UTF-8', 'de_LU.UTF-8', 'br_FR.UTF-8', 'oc_FR.UTF-8', 'ca_FR.UTF-8']
        de: ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']
        FR: ['fr(oss)']
         +: ['fr(oss)', 'de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']

    >>> _test_language_territory(show_weights=False, languageId="de", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        de: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        BE: ['nl_BE.UTF-8', 'fr_BE.UTF-8', 'de_BE.UTF-8', 'wa_BE.UTF-8', 'li_BE.UTF-8']
         +: ['de_BE.UTF-8']
        de: ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']
        BE: ['be(oss)']
         +: ['be(oss)']

    >>> _test_language_territory(show_weights=False, languageId="de", territoryId="AT") # doctest: +NORMALIZE_WHITESPACE
        de: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        AT: ['de_AT.UTF-8']
         +: ['de_AT.UTF-8']
        de: ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']
        AT: ['at(nodeadkeys)']
         +: ['at(nodeadkeys)']

    >>> _test_language_territory(show_weights=False, languageId="de", territoryId="JP") # doctest: +NORMALIZE_WHITESPACE
        de: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        JP: ['ja_JP.UTF-8']
         +: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'ja_JP.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        de: ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']
        JP: ['jp']
         +: ['jp', 'de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']

    >>> _test_language_territory(show_weights=False, languageId="ja", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ja: ['ja_JP.UTF-8']
        DE: ['de_DE.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']
         +: ['ja_JP.UTF-8', 'de_DE.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']
        ja: ['jp']
        DE: ['de(nodeadkeys)', 'de(deadacute)']
         +: ['jp', 'de(nodeadkeys)', 'de(deadacute)']

    >>> _test_language_territory(show_weights=False, languageId="de", territoryId="ZA") # doctest: +NORMALIZE_WHITESPACE
        de: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8']
        ZA: ['zu_ZA.UTF-8', 'xh_ZA.UTF-8', 'af_ZA.UTF-8', 'en_ZA.UTF-8', 'nso_ZA.UTF-8', 'tn_ZA.UTF-8', 'st_ZA.UTF-8', 'ts_ZA.UTF-8', 'ss_ZA.UTF-8', 've_ZA.UTF-8', 'nr_ZA.UTF-8']
         +: ['de_DE.UTF-8', 'de_AT.UTF-8', 'de_CH.UTF-8', 'de_IT.UTF-8', 'de_LI.UTF-8', 'de_BE.UTF-8', 'de_LU.UTF-8', 'zu_ZA.UTF-8', 'xh_ZA.UTF-8', 'af_ZA.UTF-8', 'en_ZA.UTF-8', 'nso_ZA.UTF-8', 'tn_ZA.UTF-8', 'st_ZA.UTF-8', 'ts_ZA.UTF-8', 'ss_ZA.UTF-8', 've_ZA.UTF-8', 'nr_ZA.UTF-8']
        de: ['de(nodeadkeys)', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']
        ZA: ['us(intl)', 'us', 'za']
         +: ['us(intl)', 'de(nodeadkeys)', 'us', 'za', 'de(deadacute)', 'at(nodeadkeys)', 'ch', 'be(oss)']

    >>> _test_language_territory(show_weights=False, languageId="ar", territoryId="EG") # doctest: +NORMALIZE_WHITESPACE
        ar: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']
        EG: ['ar_EG.UTF-8']
         +: ['ar_EG.UTF-8']
        ar: ['ara', 'ara(azerty)', 'iq', 'ma', 'sy']
        EG: ['ara']
         +: ['ara']

    >>> _test_language_territory(show_weights=False, languageId="ar", territoryId="IQ") # doctest: +NORMALIZE_WHITESPACE
        ar: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']
        IQ: ['ar_IQ.UTF-8']
         +: ['ar_IQ.UTF-8']
        ar: ['ara', 'ara(azerty)', 'iq', 'ma', 'sy']
        IQ: ['iq']
         +: ['iq']

    >>> _test_language_territory(show_weights=False, languageId="ar", territoryId="MA") # doctest: +NORMALIZE_WHITESPACE
        ar: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']
        MA: ['ar_MA.UTF-8', 'ber_MA.UTF-8']
         +: ['ar_MA.UTF-8']
        ar: ['ara', 'ara(azerty)', 'iq', 'ma', 'sy']
        MA: ['ma']
         +: ['ma']

    >>> _test_language_territory(show_weights=False, languageId="ar", territoryId="SY") # doctest: +NORMALIZE_WHITESPACE
        ar: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']
        SY: ['ar_SY.UTF-8']
         +: ['ar_SY.UTF-8']
        ar: ['ara', 'ara(azerty)', 'iq', 'ma', 'sy']
        SY: ['sy']
         +: ['sy']

    >>> _test_language_territory(show_weights=False, languageId="ar", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        ar: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']
        IN: ['hi_IN.UTF-8', 'en_IN.UTF-8', 'bn_IN.UTF-8', 'te_IN.UTF-8', 'mr_IN.UTF-8', 'ta_IN.UTF-8', 'ur_IN.UTF-8', 'gu_IN.UTF-8', 'kn_IN.UTF-8', 'ml_IN.UTF-8', 'or_IN.UTF-8', 'pa_IN.UTF-8', 'as_IN.UTF-8', 'mai_IN.UTF-8', 'sat_IN.UTF-8', 'ks_IN.UTF-8', 'ks_IN.UTF-8@devanagari', 'kok_IN.UTF-8', 'sd_IN.UTF-8', 'sd_IN.UTF-8@devanagari', 'doi_IN.UTF-8', 'mni_IN.UTF-8', 'brx_IN.UTF-8', 'raj_IN.UTF-8', 'mjw_IN.UTF-8', 'anp_IN.UTF-8', 'bhb_IN.UTF-8', 'bho_IN.UTF-8', 'bo_IN.UTF-8', 'hne_IN.UTF-8', 'mag_IN.UTF-8', 'tcy_IN.UTF-8', 'ar_IN.UTF-8']
         +: ['ar_IN.UTF-8']
        ar: ['ara', 'ara(azerty)', 'iq', 'ma', 'sy']
        IN: ['in(eng)']
         +: ['in(eng)', 'ara', 'ara(azerty)', 'iq', 'ma', 'sy']

    >>> _test_language_territory(show_weights=False, languageId="ar", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ar: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8']
        DE: ['de_DE.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']
         +: ['ar_EG.UTF-8', 'ar_SD.UTF-8', 'ar_DZ.UTF-8', 'ar_MA.UTF-8', 'ar_IQ.UTF-8', 'ar_SA.UTF-8', 'ar_YE.UTF-8', 'ar_SY.UTF-8', 'ar_TN.UTF-8', 'ar_LY.UTF-8', 'ar_JO.UTF-8', 'ar_AE.UTF-8', 'ar_LB.UTF-8', 'ar_KW.UTF-8', 'ar_OM.UTF-8', 'ar_QA.UTF-8', 'de_DE.UTF-8', 'ar_BH.UTF-8', 'ar_IN.UTF-8', 'ar_SS.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']
        ar: ['ara', 'ara(azerty)', 'iq', 'ma', 'sy']
        DE: ['de(nodeadkeys)', 'de(deadacute)']
         +: ['de(nodeadkeys)', 'ara', 'de(deadacute)', 'ara(azerty)', 'iq', 'ma', 'sy']

    >>> _test_language_territory(show_weights=False, languageId="as", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        as: ['as_IN.UTF-8']
        IN: ['hi_IN.UTF-8', 'en_IN.UTF-8', 'bn_IN.UTF-8', 'te_IN.UTF-8', 'mr_IN.UTF-8', 'ta_IN.UTF-8', 'ur_IN.UTF-8', 'gu_IN.UTF-8', 'kn_IN.UTF-8', 'ml_IN.UTF-8', 'or_IN.UTF-8', 'pa_IN.UTF-8', 'as_IN.UTF-8', 'mai_IN.UTF-8', 'sat_IN.UTF-8', 'ks_IN.UTF-8', 'ks_IN.UTF-8@devanagari', 'kok_IN.UTF-8', 'sd_IN.UTF-8', 'sd_IN.UTF-8@devanagari', 'doi_IN.UTF-8', 'mni_IN.UTF-8', 'brx_IN.UTF-8', 'raj_IN.UTF-8', 'mjw_IN.UTF-8', 'anp_IN.UTF-8', 'bhb_IN.UTF-8', 'bho_IN.UTF-8', 'bo_IN.UTF-8', 'hne_IN.UTF-8', 'mag_IN.UTF-8', 'tcy_IN.UTF-8', 'ar_IN.UTF-8']
         +: ['as_IN.UTF-8']
        as: ['in(eng)']
        IN: ['in(eng)']
         +: ['in(eng)']

    >>> _test_language_territory(show_weights=False, languageId="bn", territoryId="BD") # doctest: +NORMALIZE_WHITESPACE
        bn: ['bn_BD.UTF-8', 'bn_IN.UTF-8']
        BD: ['bn_BD.UTF-8']
         +: ['bn_BD.UTF-8']
        bn: ['in(eng)']
        BD: ['us']
         +: ['us', 'in(eng)']

    >>> _test_language_territory(show_weights=False, languageId="bn", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        bn: ['bn_BD.UTF-8', 'bn_IN.UTF-8']
        IN: ['hi_IN.UTF-8', 'en_IN.UTF-8', 'bn_IN.UTF-8', 'te_IN.UTF-8', 'mr_IN.UTF-8', 'ta_IN.UTF-8', 'ur_IN.UTF-8', 'gu_IN.UTF-8', 'kn_IN.UTF-8', 'ml_IN.UTF-8', 'or_IN.UTF-8', 'pa_IN.UTF-8', 'as_IN.UTF-8', 'mai_IN.UTF-8', 'sat_IN.UTF-8', 'ks_IN.UTF-8', 'ks_IN.UTF-8@devanagari', 'kok_IN.UTF-8', 'sd_IN.UTF-8', 'sd_IN.UTF-8@devanagari', 'doi_IN.UTF-8', 'mni_IN.UTF-8', 'brx_IN.UTF-8', 'raj_IN.UTF-8', 'mjw_IN.UTF-8', 'anp_IN.UTF-8', 'bhb_IN.UTF-8', 'bho_IN.UTF-8', 'bo_IN.UTF-8', 'hne_IN.UTF-8', 'mag_IN.UTF-8', 'tcy_IN.UTF-8', 'ar_IN.UTF-8']
         +: ['bn_IN.UTF-8']
        bn: ['in(eng)']
        IN: ['in(eng)']
         +: ['in(eng)']

    >>> _test_language_territory(show_weights=False, languageId="zh", territoryId="CN") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        CN: ['zh_CN.UTF-8', 'bo_CN.UTF-8', 'ug_CN.UTF-8']
         +: ['zh_CN.UTF-8']
        zh: ['cn']
        CN: ['cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", territoryId="TW") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        TW: ['zh_TW.UTF-8', 'cmn_TW.UTF-8', 'hak_TW.UTF-8', 'lzh_TW.UTF-8', 'nan_TW.UTF-8', 'nan_TW.UTF-8@latin']
         +: ['zh_TW.UTF-8']
        zh: ['cn']
        TW: ['tw']
         +: ['tw']

    >>> _test_language_territory(show_weights=False, languageId="cmn", territoryId="TW") # doctest: +NORMALIZE_WHITESPACE
        cmn: ['cmn_TW.UTF-8']
        TW: ['zh_TW.UTF-8', 'cmn_TW.UTF-8', 'hak_TW.UTF-8', 'lzh_TW.UTF-8', 'nan_TW.UTF-8', 'nan_TW.UTF-8@latin']
         +: ['cmn_TW.UTF-8']
        cmn: ['tw']
        TW: ['tw']
         +: ['tw']

    >>> _test_language_territory(show_weights=False, languageId="zh", territoryId="HK") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        HK: ['zh_HK.UTF-8', 'yue_HK.UTF-8', 'en_HK.UTF-8']
         +: ['zh_HK.UTF-8']
        zh: ['cn']
        HK: ['cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", territoryId="MO") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        MO: ['zh_HK.UTF-8']
         +: ['zh_HK.UTF-8']
        zh: ['cn']
        MO: ['cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", territoryId="SG") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        SG: ['en_SG.UTF-8', 'zh_SG.UTF-8']
         +: ['zh_SG.UTF-8']
        zh: ['cn']
        SG: ['us', 'cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="en", territoryId="SG") # doctest: +NORMALIZE_WHITESPACE
        en: ['en_US.UTF-8', 'en_GB.UTF-8', 'en_IN.UTF-8', 'en_AU.UTF-8', 'en_CA.UTF-8', 'en_DK.UTF-8', 'en_IE.UTF-8', 'en_NZ.UTF-8', 'en_NG.UTF-8', 'en_HK.UTF-8', 'en_PH.UTF-8', 'en_SG.UTF-8', 'en_ZA.UTF-8', 'en_ZM.UTF-8', 'en_ZW.UTF-8', 'en_BW.UTF-8', 'en_AG.UTF-8', 'en_IL.UTF-8']
        SG: ['en_SG.UTF-8', 'zh_SG.UTF-8']
         +: ['en_SG.UTF-8']
        en: ['us', 'gb', 'au']
        SG: ['us', 'cn']
         +: ['us']

    >>> _test_language_territory(show_weights=False, languageId="en", territoryId="AU") # doctest: +NORMALIZE_WHITESPACE
        en: ['en_US.UTF-8', 'en_GB.UTF-8', 'en_IN.UTF-8', 'en_AU.UTF-8', 'en_CA.UTF-8', 'en_DK.UTF-8', 'en_IE.UTF-8', 'en_NZ.UTF-8', 'en_NG.UTF-8', 'en_HK.UTF-8', 'en_PH.UTF-8', 'en_SG.UTF-8', 'en_ZA.UTF-8', 'en_ZM.UTF-8', 'en_ZW.UTF-8', 'en_BW.UTF-8', 'en_AG.UTF-8', 'en_IL.UTF-8']
        AU: ['en_AU.UTF-8']
         +: ['en_AU.UTF-8']
        en: ['us', 'gb', 'au']
        AU: ['au']
         +: ['au']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hant", territoryId=None) # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        None: []
         +: ['zh_TW.UTF-8', 'zh_HK.UTF-8']
        zh: ['cn']
        None: []
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hans", territoryId=None) # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        None: []
         +: ['zh_CN.UTF-8', 'zh_SG.UTF-8']
        zh: ['cn']
        None: []
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hans", territoryId="SG") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        SG: ['en_SG.UTF-8', 'zh_SG.UTF-8']
         +: ['zh_SG.UTF-8']
        zh: ['cn']
        SG: ['us', 'cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hans", territoryId="TW") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        TW: ['zh_TW.UTF-8', 'cmn_TW.UTF-8', 'hak_TW.UTF-8', 'lzh_TW.UTF-8', 'nan_TW.UTF-8', 'nan_TW.UTF-8@latin']
         +: ['zh_CN.UTF-8', 'zh_SG.UTF-8', 'zh_TW.UTF-8', 'cmn_TW.UTF-8', 'hak_TW.UTF-8', 'lzh_TW.UTF-8', 'nan_TW.UTF-8', 'nan_TW.UTF-8@latin']
        zh: ['cn']
        TW: ['tw']
         +: ['tw', 'cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hant", territoryId="HK") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        HK: ['zh_HK.UTF-8', 'yue_HK.UTF-8', 'en_HK.UTF-8']
         +: ['zh_HK.UTF-8']
        zh: ['cn']
        HK: ['cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hant", territoryId="MO") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        MO: ['zh_HK.UTF-8']
         +: ['zh_HK.UTF-8']
        zh: ['cn']
        MO: ['cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="zh", scriptId = "Hant", territoryId="CN") # doctest: +NORMALIZE_WHITESPACE
        zh: ['zh_CN.UTF-8', 'zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_SG.UTF-8']
        CN: ['zh_CN.UTF-8', 'bo_CN.UTF-8', 'ug_CN.UTF-8']
         +: ['zh_TW.UTF-8', 'zh_HK.UTF-8', 'zh_CN.UTF-8', 'bo_CN.UTF-8', 'ug_CN.UTF-8']
        zh: ['cn']
        CN: ['cn']
         +: ['cn']

    >>> _test_language_territory(show_weights=False, languageId="ia", territoryId=None) # doctest: +NORMALIZE_WHITESPACE
        ia: ['ia_FR.UTF-8']
        None: []
         +: ['ia_FR.UTF-8']
        ia: ['us(euro)']
        None: []
         +: ['us(euro)']

    >>> _test_language_territory(show_weights=False, languageId="ia", territoryId="DE") # doctest: +NORMALIZE_WHITESPACE
        ia: ['ia_FR.UTF-8']
        DE: ['de_DE.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']
         +: ['ia_FR.UTF-8', 'de_DE.UTF-8', 'nds_DE.UTF-8', 'hsb_DE.UTF-8', 'fy_DE.UTF-8', 'dsb_DE.UTF-8']
        ia: ['us(euro)']
        DE: ['de(nodeadkeys)', 'de(deadacute)']
         +: ['us(euro)', 'de(nodeadkeys)', 'de(deadacute)']

    >>> _test_language_territory(show_weights=False, languageId="tt", territoryId="RU") # doctest: +NORMALIZE_WHITESPACE
        tt: ['tt_RU.UTF-8', 'tt_RU.UTF-8@iqtelif']
        RU: ['ru_RU.UTF-8', 'ce_RU.UTF-8', 'cv_RU.UTF-8', 'mhr_RU.UTF-8', 'os_RU.UTF-8', 'tt_RU.UTF-8', 'tt_RU.UTF-8@iqtelif', 'sah_RU.UTF-8']
         +: ['tt_RU.UTF-8']
        tt: ['ru(tt)', 'us(altgr-intl)']
        RU: ['ru', 'ru(tt)', 'us(altgr-intl)']
         +: ['ru(tt)']

    >>> _test_language_territory(show_weights=False, languageId="tt", scriptId="Latn", territoryId="RU") # doctest: +NORMALIZE_WHITESPACE
        tt: ['tt_RU.UTF-8', 'tt_RU.UTF-8@iqtelif']
        RU: ['ru_RU.UTF-8', 'ce_RU.UTF-8', 'cv_RU.UTF-8', 'mhr_RU.UTF-8', 'os_RU.UTF-8', 'tt_RU.UTF-8', 'tt_RU.UTF-8@iqtelif', 'sah_RU.UTF-8']
         +: ['tt_RU.UTF-8@iqtelif']
        tt: ['ru(tt)', 'us(altgr-intl)']
        RU: ['ru', 'ru(tt)', 'us(altgr-intl)']
         +: ['us(altgr-intl)']

    # according to https://wiki.gnome.org/GnomeGoals/KeyboardData,
    # “us(euro)” keyboard should be used in NL:
    >>> _test_language_territory(show_weights=False, languageId="nl") # doctest: +NORMALIZE_WHITESPACE
        nl: ['nl_NL.UTF-8', 'nl_BE.UTF-8', 'nl_AW.UTF-8']
        None: []
         +: ['nl_NL.UTF-8', 'nl_BE.UTF-8', 'nl_AW.UTF-8']
        nl: ['us(euro)', 'us(altgr-intl)', 'be(oss)']
        None: []
         +: ['us(euro)', 'us(altgr-intl)', 'be(oss)']

    >>> _test_language_territory(show_weights=False, languageId="nl", territoryId="NL") # doctest: +NORMALIZE_WHITESPACE
        nl: ['nl_NL.UTF-8', 'nl_BE.UTF-8', 'nl_AW.UTF-8']
        NL: ['nl_NL.UTF-8', 'fy_NL.UTF-8', 'nds_NL.UTF-8', 'li_NL.UTF-8']
         +: ['nl_NL.UTF-8']
        nl: ['us(euro)', 'us(altgr-intl)', 'be(oss)']
        NL: ['us(euro)', 'us(altgr-intl)']
         +: ['us(euro)', 'us(altgr-intl)']

    # but “be(oss)” keyboard should be used for nl in BE
    # (see: https://bugzilla.redhat.com/show_bug.cgi?id=885345):
    >>> _test_language_territory(show_weights=False, languageId="nl", territoryId="BE") # doctest: +NORMALIZE_WHITESPACE
        nl: ['nl_NL.UTF-8', 'nl_BE.UTF-8', 'nl_AW.UTF-8']
        BE: ['nl_BE.UTF-8', 'fr_BE.UTF-8', 'de_BE.UTF-8', 'wa_BE.UTF-8', 'li_BE.UTF-8']
         +: ['nl_BE.UTF-8']
        nl: ['us(euro)', 'us(altgr-intl)', 'be(oss)']
        BE: ['be(oss)']
         +: ['be(oss)']

    >>> print(language_name(languageId="de")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch

    >>> print(language_name(languageId="de", territoryId="DE")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Deutschland)

    >>> print(language_name(languageId="de", territoryId="CH")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Schweiz)

    >>> print(language_name(languageId="de", territoryId="AT")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Österreich)

    >>> print(language_name(languageId="de", territoryId="BE")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Belgien)

    >>> print(language_name(languageId="de", territoryId="JP")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Japan)

    >>> print(language_name(languageId="de", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Belarus)

    >>> print(language_name(languageId="de", territoryId="BY", languageIdQuery="de", territoryIdQuery="CH")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Weissrussland)

    >>> print(language_name(languageId="de", scriptId="Latn", territoryId="DE")) # doctest: +NORMALIZE_WHITESPACE
        Deutsch (Deutschland)

    >>> print(language_name(languageId="pt")) # doctest: +NORMALIZE_WHITESPACE
        português

    >>> print(language_name(languageId="pt", territoryId="PT")) # doctest: +NORMALIZE_WHITESPACE
        português (Portugal)

    >>> print(language_name(languageId="pt", territoryId="BR")) # doctest: +NORMALIZE_WHITESPACE
        português (Brasil)

    >>> print(language_name(languageId="pt", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Portugiesisch

    >>> print(language_name(languageId="pt", territoryId="PT", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Portugiesisch (Portugal)

    >>> print(language_name(languageId="pt", territoryId="BR", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Portugiesisch (Brasilien)

    >>> print(language_name(languageId="mai", territoryId="IN", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Maithili (India)

    >>> print(language_name(languageId="mai", territoryId="NP", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Maithili (Nepal)

    >>> print(language_name(languageId="mai", territoryId="IN", languageIdQuery="mai")) # doctest: +NORMALIZE_WHITESPACE
        मैथिली (भारत)

    >>> print(language_name(languageId="mai", territoryId="NP", languageIdQuery="mai")) # doctest: +NORMALIZE_WHITESPACE
        मैथिली (नेपाल)

    >>> print(language_name(languageId="zh")) # doctest: +NORMALIZE_WHITESPACE
        中文

    >>> print(language_name(languageId="zh", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Chinesisch

    >>> print(language_name(languageId="zh", scriptId="Hant", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Chinesisch (traditionell)

    >>> print(language_name(languageId="zh", scriptId="Hans", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Chinesisch (vereinfacht)

    >>> print(language_name(languageId="zh", territoryId="HK", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Traditionelles Chinesisch (Sonderverwaltungszone Hongkong)

    >>> print(language_name(languageId="zh", territoryId="MO", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Traditionelles Chinesisch (Sonderverwaltungszone Macao)

    >>> print(language_name(languageId="zh", territoryId="MO", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Traditional Chinese (Macau SAR China)

    >>> print(language_name(languageId="zh", territoryId="SG", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Vereinfachtes Chinesisch (Singapur)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Traditionelles Chinesisch (Taiwan)

    >>> print(language_name(languageId="zh", territoryId="CN")) # doctest: +NORMALIZE_WHITESPACE
        简体中文 (中国)

    >>> print(language_name(languageId="zh", territoryId="SG")) # doctest: +NORMALIZE_WHITESPACE
        简体中文 (新加坡)

    >>> print(language_name(languageId="zh", territoryId="TW")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (台灣)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Traditional Chinese (Republic of China)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Traditionelles Chinesisch (Taiwan)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="de", territoryIdQuery="DE")) # doctest: +NORMALIZE_WHITESPACE
        Traditionelles Chinesisch (Taiwan)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="es")) # doctest: +NORMALIZE_WHITESPACE
        chino tradicional (Taiwán)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="es", territoryIdQuery="ES")) # doctest: +NORMALIZE_WHITESPACE
        chino tradicional (Taiwán)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="zh")) # doctest: +NORMALIZE_WHITESPACE
        繁体中文 (台湾)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="zh", territoryIdQuery="TW")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (台灣)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="zh", territoryIdQuery="CN")) # doctest: +NORMALIZE_WHITESPACE
        繁体中文 (中华民国)

    >>> print(language_name(languageId="zh", territoryId="HK")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (中華人民共和國香港特別行政區)

    >>> print(language_name(languageId="zh", territoryId="MO")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (中華人民共和國澳門特別行政區)

    >>> print(language_name(languageId="zh", scriptId="Hans", territoryId="CN")) # doctest: +NORMALIZE_WHITESPACE
        简体中文 (中国)

    >>> print(language_name(languageId="zh", scriptId="Hans", territoryId="SG")) # doctest: +NORMALIZE_WHITESPACE
        简体中文 (新加坡)

    >>> print(language_name(languageId="zh", scriptId="Hant", territoryId="TW")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (台灣)

    >>> print(language_name(languageId="zh", scriptId="Hant", territoryId="HK")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (中華人民共和國香港特別行政區)

    >>> print(language_name(languageId="zh", scriptId="Hant", territoryId="MO")) # doctest: +NORMALIZE_WHITESPACE
        繁體中文 (中華人民共和國澳門特別行政區)

    >>> print(language_name(languageId="sr")) # doctest: +NORMALIZE_WHITESPACE
        српски

    >>> print(language_name(languageId="sr", territoryId="RS")) # doctest: +NORMALIZE_WHITESPACE
        српски (Србија)

    >>> print(language_name(languageId="sr", territoryId="ME")) # doctest: +NORMALIZE_WHITESPACE
        српски (Црна Гора)

    >>> print(language_name(languageId="sr", scriptId="Cyrl")) # doctest: +NORMALIZE_WHITESPACE
        српски (Ћирилица)

    >>> print(language_name(languageId="sr", scriptId="Latn")) # doctest: +NORMALIZE_WHITESPACE
        Srpski (Latinica)

    >>> print(language_name(languageId="sr", scriptId="Cyrl", territoryId="RS")) # doctest: +NORMALIZE_WHITESPACE
        српски (Ћирилица) (Србија)

    >>> print(language_name(languageId="sr", scriptId="Latn", territoryId="RS")) # doctest: +NORMALIZE_WHITESPACE
        Srpski (Latinica) (Srbija)

    >>> print(language_name(languageId="sr", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Serbian

    >>> print(language_name(languageId="sr", territoryId="RS", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Serbian (Serbia)

    >>> print(language_name(languageId="sr", territoryId="ME", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Serbian (Montenegro)

    >>> print(language_name(languageId="sr", scriptId="Cyrl", territoryId="RS", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Serbian (Cyrillic) (Serbia)

    >>> print(language_name(languageId="sr", scriptId="Latn", territoryId="RS", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Serbian (Latin) (Serbia)

    # script and territory given in languageId override script and territory in extra parameters:
    >>> print(language_name(languageId="sr_Latn_RS", scriptId="Cyrl", territoryId="DE", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Serbian (Latin) (Serbia)

    >>> print(language_name(languageId="be")) # doctest: +NORMALIZE_WHITESPACE
        беларуская

    >>> print(language_name(languageId="be", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        беларуская (Беларусь)

    >>> print(language_name(languageId="be", scriptId="Cyrl")) # doctest: +NORMALIZE_WHITESPACE
        беларуская

    >>> print(language_name(languageId="be", scriptId="Latn")) # doctest: +NORMALIZE_WHITESPACE
        biełaruskaja

    >>> print(language_name(languageId="be", scriptId="latin", languageIdQuery="be", scriptIdQuery="latin")) # doctest: +NORMALIZE_WHITESPACE
        biełaruskaja

    >>> print(language_name(languageId="be", scriptId="Cyrl", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        беларуская (Беларусь)

    >>> print(language_name(languageId="be", scriptId="Latn", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        biełaruskaja (Bielaruś)

    >>> print(language_name(languageId="be", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Belarusian

    >>> print(language_name(languageId="be", territoryId="BY", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Belarusian (Belarus)

    >>> print(language_name(languageId="be", scriptId="Cyrl", territoryId="BY", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Belarusian (Belarus)

    >>> print(language_name(languageId="be", scriptId="Latn", territoryId="BY", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Belarusian (Belarus)

    # script and territory given in languageId override script and territory in extra parameters:
    >>> print(language_name(languageId="be_Latn_BY", scriptId="Cyrl", territoryId="DE", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        Belarusian (Belarus)

    >>> print(language_name(languageId="nds", territoryId="DE")) # doctest: +NORMALIZE_WHITESPACE
        Neddersass’sch (Düütschland)

    >>> print(language_name(languageId="nds", territoryId="NL")) # doctest: +NORMALIZE_WHITESPACE
        Neddersass’sch (Nedderlannen)

    >>> print(language_name(languageId="pa")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ

    >>> print(language_name(languageId="pa", territoryId="PK")) # doctest: +NORMALIZE_WHITESPACE
        پنجاب (پکستان)

    >>> print(language_name(languageId="pa", scriptId="Arab", territoryId="PK")) # doctest: +NORMALIZE_WHITESPACE
        پنجاب (پکستان)

    >>> print(language_name(languageId="pa", territoryId="IN")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ (ਭਾਰਤ)

    >>> print(language_name(languageId="pa", scriptId="Guru", territoryId="IN")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ (ਭਾਰਤ)

    >>> print(language_name(languageId="pa", scriptId="Arab")) # doctest: +NORMALIZE_WHITESPACE
        پنجاب

    >>> print(language_name(languageId="pa", scriptId="Guru")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ

    >>> print(language_name(languageId="tl")) # doctest: +NORMALIZE_WHITESPACE
        Tagalog

    >>> print(language_name(languageId="ca")) # doctest: +NORMALIZE_WHITESPACE
    català

    >>> print(language_name(languageId="ca_AD")) # doctest: +NORMALIZE_WHITESPACE
    català (Andorra)

    >>> print(language_name(languageId="ca_FR")) # doctest: +NORMALIZE_WHITESPACE
    català (França)

    >>> print(language_name(languageId="ca_IT")) # doctest: +NORMALIZE_WHITESPACE
    català (Itàlia)

    >>> print(language_name(languageId="ca_ES")) # doctest: +NORMALIZE_WHITESPACE
    català (Espanya)

    >>> print(language_name(languageId="ca_ES.UTF-8")) # doctest: +NORMALIZE_WHITESPACE
    català (Espanya)

    >>> print(language_name(languageId="ca_ES_VALENCIA")) # doctest: +NORMALIZE_WHITESPACE
    valencià (Espanya)

    >>> print(language_name(languageId="ca_ES@valencia")) # doctest: +NORMALIZE_WHITESPACE
    valencià (Espanya)

    >>> print(language_name(languageId="ca_ES.UTF-8@valencia")) # doctest: +NORMALIZE_WHITESPACE
    valencià (Espanya)

    >>> print(territory_name(territoryId="AE", languageIdQuery="ar")) # doctest: +NORMALIZE_WHITESPACE
        الإمارات العربية المتحدة

    >>> print(territory_name(territoryId="AE", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Vereinigte Arabische Emirate

    >>> print(territory_name(territoryId="AE", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        United Arab Emirates

    >>> print(territory_name(territoryId="AE", languageIdQuery=None)) # doctest: +NORMALIZE_WHITESPACE

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh")) # doctest: +NORMALIZE_WHITESPACE
        台湾

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", scriptIdQuery="Hant")) # doctest: +NORMALIZE_WHITESPACE
        台灣

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", scriptIdQuery="Hant", territoryIdQuery="TW")) # doctest: +NORMALIZE_WHITESPACE
        台灣

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", territoryIdQuery="TW")) # doctest: +NORMALIZE_WHITESPACE
        台灣

    >>> print(territory_name(territoryId="HK", languageIdQuery="zh", territoryIdQuery="HK")) # doctest: +NORMALIZE_WHITESPACE
        中國香港特別行政區

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", scriptIdQuery="Hans")) # doctest: +NORMALIZE_WHITESPACE
        台湾

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", scriptIdQuery="Hans", territoryIdQuery="CN")) # doctest: +NORMALIZE_WHITESPACE
        中华民国

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", territoryIdQuery="CN")) # doctest: +NORMALIZE_WHITESPACE
        中华民国

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", scriptIdQuery="Cyrl", territoryIdQuery="CN")) # doctest: +NORMALIZE_WHITESPACE
        中华民国

    >>> print(territory_name(territoryId="TW", languageIdQuery="zh", scriptIdQuery="Hans", territoryIdQuery="DE")) # doctest: +NORMALIZE_WHITESPACE
        台湾

    >>> print(territory_name(territoryId="TW", languageIdQuery="de", scriptIdQuery="Latn", territoryIdQuery="DE")) # doctest: +NORMALIZE_WHITESPACE
        Taiwan

    >>> print(territory_name(territoryId="CH", languageIdQuery="de", scriptIdQuery="Latn", territoryIdQuery="DE")) # doctest: +NORMALIZE_WHITESPACE
        Schweiz

    >>> print(territory_name(territoryId="BY", languageIdQuery="de", scriptIdQuery="Latn", territoryIdQuery="CH")) # doctest: +NORMALIZE_WHITESPACE
        Weissrussland

    # script given in languageIdQuery overrides script given in scriptIdQuery:
    >>> print(territory_name(territoryId="RS", languageIdQuery="sr_Cyrl_RS", scriptIdQuery="Latn", territoryIdQuery="CH")) # doctest: +NORMALIZE_WHITESPACE
        Србија

    >>> print(territory_name(territoryId="CY", languageIdQuery="tr")) # doctest: +NORMALIZE_WHITESPACE
        Kıbrıs

    >>> print(territory_name(territoryId="CY", languageIdQuery="tr_CY")) # doctest: +NORMALIZE_WHITESPACE
        Kıbrıs

    ######################################################################
    # testing locale pattern regexp:
    #  valid patterns:

    >>> _test_cldr_locale_pattern(localeId="srx_XK") # doctest: +NORMALIZE_WHITESPACE
        [('language', 'srx'), ('script', None), ('territory', 'XK')]

    >>> _test_cldr_locale_pattern(localeId="sr_XK") # doctest: +NORMALIZE_WHITESPACE
        [('language', 'sr'), ('script', None), ('territory', 'XK')]

    >>> _test_cldr_locale_pattern(localeId="sr@foo") # doctest: +NORMALIZE_WHITESPACE
        [('language', 'sr'), ('script', None), ('territory', None)]

    >>> _test_cldr_locale_pattern(localeId="sr_Cyrl_RS") # doctest: +NORMALIZE_WHITESPACE
        [('language', 'sr'), ('script', 'Cyrl'), ('territory', 'RS')]

    >>> _test_cldr_locale_pattern(localeId="sr_Cyrl_RS@foo") # doctest: +NORMALIZE_WHITESPACE
        [('language', 'sr'), ('script', 'Cyrl'), ('territory', 'RS')]

    >>> _test_cldr_locale_pattern(localeId="srx_Artc_XK") # doctest: +NORMALIZE_WHITESPACE
        [('language', 'srx'), ('script', 'Artc'), ('territory', 'XK')]

    #----------------------------------------------------------------------
    # invalid patterns:
    >>> _test_cldr_locale_pattern(localeId="srxf_Artc_XK") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> _test_cldr_locale_pattern(localeId="srx_ARtc_XK") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> _test_cldr_locale_pattern(localeId="srx_Artc_XXk") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> _test_cldr_locale_pattern(localeId="srx_XXk") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> _test_cldr_locale_pattern(localeId="srx_Artc_Kx") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> supports_ascii("jp") # doctest: +NORMALIZE_WHITESPACE
        True

    >>> supports_ascii("ru") # doctest: +NORMALIZE_WHITESPACE
        False

    >>> supports_ascii("cz") # doctest: +NORMALIZE_WHITESPACE
        True

    >>> supports_ascii("sk") # doctest: +NORMALIZE_WHITESPACE
        True

    >>> supports_ascii("ara") # doctest: +NORMALIZE_WHITESPACE
        False

    >>> supports_ascii("not_existing_in_database") # doctest: +NORMALIZE_WHITESPACE
        True

    >>> languageId("Sindhi")  # doctest: +NORMALIZE_WHITESPACE
        'sd'

    >>> languageId("Српски")  # doctest: +NORMALIZE_WHITESPACE
        'sr'

    >>> languageId("Serbian")  # doctest: +NORMALIZE_WHITESPACE
        'sr'

    >>> languageId("Serbian (Cyrillic)")  # doctest: +NORMALIZE_WHITESPACE
        'sr_Cyrl'

    >>> languageId("Serbian (Latin)")  # doctest: +NORMALIZE_WHITESPACE
        'sr_Latn'

    >>> languageId("Српски (Ћирилица)")  # doctest: +NORMALIZE_WHITESPACE
        'sr_Cyrl'

    >>> languageId("Српски (Србија)")  # doctest: +NORMALIZE_WHITESPACE
        'sr_RS'

    >>> languageId("Portuguese")  # doctest: +NORMALIZE_WHITESPACE
        'pt'

    >>> languageId("Portuguese (Brazil)")  # doctest: +NORMALIZE_WHITESPACE
        'pt_BR'

    >>> languageId("Portuguese (Portugal)")  # doctest: +NORMALIZE_WHITESPACE
        'pt_PT'

    >>> languageId("Portugiesisch (Brasilien)")  # doctest: +NORMALIZE_WHITESPACE
        'pt_BR'

    >>> languageId("Shuswap language")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("Shuswap Language")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("shuswap language")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("sHuSwAp laNguAge")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("Czech (Czech Republic)")  # doctest: +NORMALIZE_WHITESPACE
        'cs_CZ'

    >>> languageId("English (United Kingdom)")  # doctest: +NORMALIZE_WHITESPACE
        'en_GB'

    >>> languageId("Low German (Germany)")  # doctest: +NORMALIZE_WHITESPACE
        'nds_DE'

    >>> languageId("Tagalog")  # doctest: +NORMALIZE_WHITESPACE
        'tl'

    >>> languageId("Filipino")  # doctest: +NORMALIZE_WHITESPACE
        'fil'

    >>> print(langtable.timezone_name(timezoneId='US/Mountain', languageIdQuery='ja'))  # doctest: +NORMALIZE_WHITESPACE
       アメリカ合衆国/山地時間

    >>> print(langtable.timezone_name(timezoneId='US/Pacific', languageIdQuery='ja'))  # doctest: +NORMALIZE_WHITESPACE
       アメリカ合衆国/太平洋時間

    >>> print(langtable.timezone_name(timezoneId='America/North_Dakota/Center', languageIdQuery='es'))  # doctest: +NORMALIZE_WHITESPACE
        América/Dakota del Norte/Centro

    >>> print(langtable.timezone_name(timezoneId='Europe/Berlin', languageIdQuery='zh'))  # doctest: +NORMALIZE_WHITESPACE
        欧洲/柏林

    >>> print(langtable.timezone_name(timezoneId='Europe/Berlin', languageIdQuery='zh_Hant'))  # doctest: +NORMALIZE_WHITESPACE
       歐洲/柏林

    >>> print(langtable.timezone_name(timezoneId='Europe/Berlin', languageIdQuery='zh_CN'))  # doctest: +NORMALIZE_WHITESPACE
        欧洲/柏林

    >>> print(langtable.timezone_name(timezoneId='Europe/Berlin', languageIdQuery='zh_TW'))  # doctest: +NORMALIZE_WHITESPACE
        歐洲/柏林

    >>> print(langtable.timezone_name(timezoneId='GMT+1', languageIdQuery='cs'))  # doctest: +NORMALIZE_WHITESPACE
        GMT+1

    >>> print(langtable.timezone_name(timezoneId='foo/bar', languageIdQuery='cs'))  # doctest: +NORMALIZE_WHITESPACE
        foo/bar

    >>> print(langtable.timezone_name(timezoneId='Europe/foo/bar', languageIdQuery='cs'))  # doctest: +NORMALIZE_WHITESPACE
        Evropa/foo/bar

    >>> print(langtable.timezone_name(timezoneId='America/Vancouver', languageIdQuery='xxx'))  # doctest: +NORMALIZE_WHITESPACE
        America/Vancouver

    >>> print(langtable.timezone_name(timezoneId='Pacific/Pago_Pago', languageIdQuery='xxx'))  # doctest: +NORMALIZE_WHITESPACE
        Pacific/Pago_Pago

    >>> print(langtable.timezone_name(timezoneId='America/Vancouver', languageIdQuery='ast'))  # doctest: +NORMALIZE_WHITESPACE
        América/Vancouver

    >>> print(langtable.timezone_name(timezoneId='Pacific/Pago_Pago', languageIdQuery='ast'))  # doctest: +NORMALIZE_WHITESPACE
        Océanu Pacíficu/Pago Pago
    '''

if __name__ == "__main__":
    import doctest
    (FAILED, ATTEMPTED) = doctest.testmod()
    if FAILED:
        # Return number of failed tests:
        sys.exit(FAILED)
    sys.exit(0)
