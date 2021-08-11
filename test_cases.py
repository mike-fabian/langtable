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
    >>> from langtable import list_common_languages
    >>> from langtable import list_common_keyboards

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
        ['ibus/m17n:as:inscript2']

    >>> list_inputmethods(languageId="as", territoryId="BD") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:as:inscript2']

    >>> list_inputmethods(languageId="bn") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:bn:inscript2']

    >>> list_inputmethods(languageId="gu") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:gu:inscript2']

    >>> list_inputmethods(languageId="hi") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:hi:inscript2']

    >>> list_inputmethods(languageId="kn") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:kn:inscript2']

    >>> list_inputmethods(languageId="mai") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:mai:inscript2']

    >>> list_inputmethods(languageId="ml") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:ml:inscript2']

    >>> list_inputmethods(languageId="mr") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:mr:inscript2']

    >>> list_inputmethods(languageId="or") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:or:inscript2']

    >>> list_inputmethods(languageId="pa") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:pa:inscript2-guru']

    >>> list_inputmethods(languageId="ta") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:ta:inscript2']

    >>> list_inputmethods(languageId="te") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:te:inscript2']

    >>> list_inputmethods(languageId="ur") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:ur:phonetic']

    >>> list_inputmethods(languageId="sd") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript2-deva']

    >>> list_inputmethods(languageId="sd", scriptId="Deva") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript2-deva']

    >>> list_inputmethods(languageId="sd", scriptId="Arab") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_inputmethods(languageId="sd", scriptId="Deva", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript2-deva']

    >>> list_inputmethods(languageId="sd", scriptId="Arab", territoryId="PK") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_inputmethods(languageId="sd", scriptId="Deva", territoryId="PK") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript2-deva']

    >>> list_inputmethods(languageId="sd", scriptId="Arab", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        []

    >>> list_inputmethods(languageId="sd", territoryId="PK") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript2-deva']

    >>> list_inputmethods(languageId="sd", territoryId="IN") # doctest: +NORMALIZE_WHITESPACE
        ['ibus/m17n:sd:inscript2-deva']

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
        Português

    >>> print(language_name(languageId="pt", territoryId="PT")) # doctest: +NORMALIZE_WHITESPACE
        Português (Portugal)

    >>> print(language_name(languageId="pt", territoryId="BR")) # doctest: +NORMALIZE_WHITESPACE
        Português (Brasil)

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
        Mandarin (traditionell)

    >>> print(language_name(languageId="zh", scriptId="Hans", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Mandarin (Vereinfacht)

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
        Chino mandarín tradicional (Taiwán)

    >>> print(language_name(languageId="zh", territoryId="TW", languageIdQuery="es", territoryIdQuery="ES")) # doctest: +NORMALIZE_WHITESPACE
        Chino mandarín tradicional (Taiwán)

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
        Српски

    >>> print(language_name(languageId="sr", territoryId="RS")) # doctest: +NORMALIZE_WHITESPACE
        Српски (Србија)

    >>> print(language_name(languageId="sr", territoryId="ME")) # doctest: +NORMALIZE_WHITESPACE
        Српски (Црна Гора)

    >>> print(language_name(languageId="sr", scriptId="Cyrl")) # doctest: +NORMALIZE_WHITESPACE
        Српски (Ћирилица)

    >>> print(language_name(languageId="sr", scriptId="Latn")) # doctest: +NORMALIZE_WHITESPACE
        Srpski (Latinica)

    >>> print(language_name(languageId="sr", scriptId="Cyrl", territoryId="RS")) # doctest: +NORMALIZE_WHITESPACE
        Српски (Ћирилица) (Србија)

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
        Беларуская

    >>> print(language_name(languageId="be", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        Беларуская (Беларусь)

    >>> print(language_name(languageId="be", scriptId="Cyrl")) # doctest: +NORMALIZE_WHITESPACE
        Беларуская

    >>> print(language_name(languageId="be", scriptId="Latn")) # doctest: +NORMALIZE_WHITESPACE
        Biełaruskaja

    >>> print(language_name(languageId="be", scriptId="latin", languageIdQuery="be", scriptIdQuery="latin")) # doctest: +NORMALIZE_WHITESPACE
        Biełaruskaja

    >>> print(language_name(languageId="be", scriptId="Cyrl", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        Беларуская (Беларусь)

    >>> print(language_name(languageId="be", scriptId="Latn", territoryId="BY")) # doctest: +NORMALIZE_WHITESPACE
        Biełaruskaja (Biełaruś)

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
        پنجابی (پکستان)

    >>> print(language_name(languageId="pa", scriptId="Arab", territoryId="PK")) # doctest: +NORMALIZE_WHITESPACE
        پنجابی (پکستان)

    >>> print(language_name(languageId="pa", territoryId="IN")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ (ਭਾਰਤ)

    >>> print(language_name(languageId="pa", scriptId="Guru", territoryId="IN")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ (ਭਾਰਤ)

    >>> print(language_name(languageId="pa", scriptId="Arab")) # doctest: +NORMALIZE_WHITESPACE
        پنجابی

    >>> print(language_name(languageId="pa", scriptId="Guru")) # doctest: +NORMALIZE_WHITESPACE
        ਪੰਜਾਬੀ

    >>> print(language_name(languageId="tl")) # doctest: +NORMALIZE_WHITESPACE
        Tagalog

    >>> print(language_name(languageId="ca")) # doctest: +NORMALIZE_WHITESPACE
    Català

    >>> print(language_name(languageId="ca_AD")) # doctest: +NORMALIZE_WHITESPACE
    Català (Andorra)

    >>> print(language_name(languageId="ca_FR")) # doctest: +NORMALIZE_WHITESPACE
    Català (França)

    >>> print(language_name(languageId="ca_IT")) # doctest: +NORMALIZE_WHITESPACE
    Català (Itàlia)

    >>> print(language_name(languageId="ca_ES")) # doctest: +NORMALIZE_WHITESPACE
    Català (Espanya)

    >>> print(language_name(languageId="ca_ES.UTF-8")) # doctest: +NORMALIZE_WHITESPACE
    Català (Espanya)

    >>> print(language_name(languageId="ca_ES_VALENCIA")) # doctest: +NORMALIZE_WHITESPACE
    Valencià (Espanya)

    >>> print(language_name(languageId="ca_ES@valencia")) # doctest: +NORMALIZE_WHITESPACE
    Valencià (Espanya)

    >>> print(language_name(languageId="ca_ES.UTF-8@valencia")) # doctest: +NORMALIZE_WHITESPACE
    Valencià (Espanya)

    ######################################################################
    # Test the fallback flag:
    >>> print(language_name(languageId="de", languageIdQuery="quz")) # doctest: +NORMALIZE_WHITESPACE
    German

    >>> print(language_name(languageId="de", languageIdQuery="quz", fallback=False)) # doctest: +NORMALIZE_WHITESPACE

    ######################################################################
    >>> print(language_name(languageId="sr_RS.UTF-8@latin")) # doctest: +NORMALIZE_WHITESPACE
    Srpski (Latinica) (Srbija)

    >>> print(language_name(languageId="sr_RS.utf8@latin")) # doctest: +NORMALIZE_WHITESPACE
    Srpski (Latinica) (Srbija)

    >>> print(language_name(languageId="aa_DJ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Qafar (Yabuuti)
    >>> print(language_name(languageId="aa_ER.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Qafar (Eretria)
    >>> print(language_name(languageId="aa_ER.utf8@saaho")) # doctest: +NORMALIZE_WHITESPACE
    Qafar (Eretria)
    >>> print(language_name(languageId="aa_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Qafar (Otobbia)
    >>> print(language_name(languageId="af_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Afrikaans (Suid-Afrika)
    >>> print(language_name(languageId="agr_PE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Awajún (Perú)
    >>> print(language_name(languageId="ak_GH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Akan (Gaana)
    >>> print(language_name(languageId="am_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    አማርኛ (ኢትዮጵያ)
    >>> print(language_name(languageId="an_ES.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Aragonés (Espanya)
    >>> print(language_name(languageId="anp_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    अंगिका (भारत)
    >>> print(language_name(languageId="ar_AE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (الإمارات العربية المتحدة)
    >>> print(language_name(languageId="ar_BH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (البحرين)
    >>> print(language_name(languageId="ar_DZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (الجزائر)
    >>> print(language_name(languageId="ar_EG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (مصر)
    >>> print(language_name(languageId="ar_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (الهند)
    >>> print(language_name(languageId="ar_IQ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (العراق)
    >>> print(language_name(languageId="ar_JO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (الأردن)
    >>> print(language_name(languageId="ar_KW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (الكويت)
    >>> print(language_name(languageId="ar_LB.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (لبنان)
    >>> print(language_name(languageId="ar_LY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (ليبيا)
    >>> print(language_name(languageId="ar_MA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (المغرب)
    >>> print(language_name(languageId="ar_OM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (عُمان)
    >>> print(language_name(languageId="ar_QA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (قطر)
    >>> print(language_name(languageId="ar_SA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (المملكة العربية السعودية)
    >>> print(language_name(languageId="ar_SD.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (السودان)
    >>> print(language_name(languageId="ar_SS.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (جنوب السودان)
    >>> print(language_name(languageId="ar_SY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (سوريا)
    >>> print(language_name(languageId="ar_TN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (تونس)
    >>> print(language_name(languageId="ar_YE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    العربية (اليمن)
    >>> print(language_name(languageId="as_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    অসমীয়া (ভাৰত)
    >>> print(language_name(languageId="ast_ES.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Asturianu (España)
    >>> print(language_name(languageId="ayc_PE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Aymar aru (Piruw)
    >>> print(language_name(languageId="az_AZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Azərbaycan (Azərbaycan)
    >>> print(language_name(languageId="az_IR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    تۆرکجه (ایران)
    >>> print(language_name(languageId="be_BY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Беларуская (Беларусь)
    >>> print(language_name(languageId="be_BY.utf8@latin")) # doctest: +NORMALIZE_WHITESPACE
    Biełaruskaja (Biełaruś)
    >>> print(language_name(languageId="bem_ZM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ichibemba (Zambia)
    >>> print(language_name(languageId="ber_DZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Tamaziɣt (Lezzayer)
    >>> print(language_name(languageId="ber_MA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ⵜⴰⵎⴰⵣⵉⵖⵜ (ⵜⴰⴳⵍⴷⵉⵜ ⵏ ⵍⵎⵖⵔⵉⴱ)
    >>> print(language_name(languageId="bg_BG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Български (България)
    >>> print(language_name(languageId="bhb_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    भीली (भारत)
    >>> print(language_name(languageId="bho_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    भोजपुरी (भारत)
    >>> print(language_name(languageId="bho_NP.utf8")) # doctest: +NORMALIZE_WHITESPACE
    भोजपुरी (नेपाल)
    >>> print(language_name(languageId="bi_VU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Bislama (Vanuatu)
    >>> print(language_name(languageId="bn_BD.utf8")) # doctest: +NORMALIZE_WHITESPACE
    বাংলা (বাংলাদেশ)
    >>> print(language_name(languageId="bn_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    বাংলা (ভারত)
    >>> print(language_name(languageId="bo_CN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    བོད་སྐད་ (རྒྱ་ནག)
    >>> print(language_name(languageId="bo_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    བོད་སྐད་ (རྒྱ་གར་)
    >>> print(language_name(languageId="br_FR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Brezhoneg (Frañs)
    >>> print(language_name(languageId="brx_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    बड़ो (भारत)
    >>> print(language_name(languageId="bs_BA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Bosanski (Bosna i Hercegovina)
    >>> print(language_name(languageId="byn_ER.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ብሊን (ኤርትራ)
    >>> print(language_name(languageId="ca_AD.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Català (Andorra)
    >>> print(language_name(languageId="ca_ES.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Català (Espanya)
    >>> print(language_name(languageId="ca_ES.utf8@valencia")) # doctest: +NORMALIZE_WHITESPACE
    Valencià (Espanya)
    >>> print(language_name(languageId="ca_FR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Català (França)
    >>> print(language_name(languageId="ca_IT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Català (Itàlia)
    >>> print(language_name(languageId="ce_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Нохчийн (Росси)
    >>> print(language_name(languageId="chr_US.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ᏣᎳᎩ (ᏌᏊ ᎢᏳᎾᎵᏍᏔᏅ ᏍᎦᏚᎩ)
    >>> print(language_name(languageId="cmn_TW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    漢語官話 (中華民國)
    >>> print(language_name(languageId="crh_UA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Qırımtatar tili (Ukraine)
    >>> print(language_name(languageId="cs_CZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Čeština (Česko)
    >>> print(language_name(languageId="csb_PL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kaszëbsczi jãzëk (Pòlskô)
    >>> print(language_name(languageId="cv_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Чӑвашла (Russia)
    >>> print(language_name(languageId="cy_GB.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Cymraeg (Y Deyrnas Unedig)
    >>> print(language_name(languageId="da_DK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Dansk (Danmark)
    >>> print(language_name(languageId="de_AT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Österreich)
    >>> print(language_name(languageId="de_BE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Belgien)
    >>> print(language_name(languageId="de_CH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Schweiz)
    >>> print(language_name(languageId="de_DE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Deutschland)
    >>> print(language_name(languageId="de_IT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Italien)
    >>> print(language_name(languageId="de_LI.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Liechtenstein)
    >>> print(language_name(languageId="de_LU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Deutsch (Luxemburg)
    >>> print(language_name(languageId="doi_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    डोगरी (भारत)
    >>> print(language_name(languageId="dsb_DE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Dolnoserbšćina (Nimska)
    >>> print(language_name(languageId="dv_MV.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ދިވެހި (ދިވެހިރާއްޖެ)
    >>> print(language_name(languageId="dz_BT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    རྫོང་ཁ (འབྲུག)
    >>> print(language_name(languageId="el_CY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ελληνικά (Κύπρος)
    >>> print(language_name(languageId="el_GR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ελληνικά (Ελλάδα)
    >>> print(language_name(languageId="en_AG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Antigua & Barbuda)
    >>> print(language_name(languageId="en_AU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Australia)
    >>> print(language_name(languageId="en_BW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Botswana)
    >>> print(language_name(languageId="en_CA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Canada)
    >>> print(language_name(languageId="en_DK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Denmark)
    >>> print(language_name(languageId="en_GB.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (United Kingdom)
    >>> print(language_name(languageId="en_HK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Hong Kong SAR China)
    >>> print(language_name(languageId="en_IE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Ireland)
    >>> print(language_name(languageId="en_IL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Israel)
    >>> print(language_name(languageId="en_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (India)
    >>> print(language_name(languageId="en_NG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Nigeria)
    >>> print(language_name(languageId="en_NZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (New Zealand)
    >>> print(language_name(languageId="en_PH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Philippines)
    >>> print(language_name(languageId="en_SC.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Seychelles)
    >>> print(language_name(languageId="en_SG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Singapore)
    >>> print(language_name(languageId="en_US.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (United States)
    >>> print(language_name(languageId="en_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (South Africa)
    >>> print(language_name(languageId="en_ZM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Zambia)
    >>> print(language_name(languageId="en_ZW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    English (Zimbabwe)
    >>> print(language_name(languageId="eo.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Esperanto
    >>> print(language_name(languageId="es_AR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Argentina)
    >>> print(language_name(languageId="es_BO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Bolivia)
    >>> print(language_name(languageId="es_CL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Chile)
    >>> print(language_name(languageId="es_CO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Colombia)
    >>> print(language_name(languageId="es_CR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Costa Rica)
    >>> print(language_name(languageId="es_CU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Cuba)
    >>> print(language_name(languageId="es_DO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (República Dominicana)
    >>> print(language_name(languageId="es_EC.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Ecuador)
    >>> print(language_name(languageId="es_ES.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (España)
    >>> print(language_name(languageId="es_GT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Guatemala)
    >>> print(language_name(languageId="es_HN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Honduras)
    >>> print(language_name(languageId="es_MX.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (México)
    >>> print(language_name(languageId="es_NI.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Nicaragua)
    >>> print(language_name(languageId="es_PA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Panamá)
    >>> print(language_name(languageId="es_PE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Perú)
    >>> print(language_name(languageId="es_PR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Puerto Rico)
    >>> print(language_name(languageId="es_PY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Paraguay)
    >>> print(language_name(languageId="es_SV.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (El Salvador)
    >>> print(language_name(languageId="es_US.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Estados Unidos)
    >>> print(language_name(languageId="es_UY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Uruguay)
    >>> print(language_name(languageId="es_VE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Español (Venezuela)
    >>> print(language_name(languageId="et_EE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Eesti (Eesti)
    >>> print(language_name(languageId="eu_ES.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Euskara (Espainia)
    >>> print(language_name(languageId="fa_IR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    فارسی (ایران)
    >>> print(language_name(languageId="ff_SN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Pulaar (Senegaal)
    >>> print(language_name(languageId="fi_FI.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Suomi (Suomi)
    >>> print(language_name(languageId="fil_PH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Filipino (Pilipinas)
    >>> print(language_name(languageId="fo_FO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Føroyskt (Føroyar)
    >>> print(language_name(languageId="fr_BE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Français (Belgique)
    >>> print(language_name(languageId="fr_CA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Français (Canada)
    >>> print(language_name(languageId="fr_CH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Français (Suisse)
    >>> print(language_name(languageId="fr_FR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Français (France)
    >>> print(language_name(languageId="fr_LU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Français (Luxembourg)
    >>> print(language_name(languageId="fur_IT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Furlan (Italie)
    >>> print(language_name(languageId="fy_DE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Frysk (Dútslân)
    >>> print(language_name(languageId="fy_NL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    West-Frysk (Nederlân)
    >>> print(language_name(languageId="ga_IE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Gaeilge (Éire)
    >>> print(language_name(languageId="gd_GB.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Gàidhlig (An Rìoghachd Aonaichte)
    >>> print(language_name(languageId="gez_ER.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ግዕዝ (ኤርትራ)
    >>> print(language_name(languageId="gez_ER.utf8@abegede")) # doctest: +NORMALIZE_WHITESPACE
    ግዕዝ (ኤርትራ)
    >>> print(language_name(languageId="gez_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ግዕዝ (ኢትዮጵያ)
    >>> print(language_name(languageId="gez_ET.utf8@abegede")) # doctest: +NORMALIZE_WHITESPACE
    ግዕዝ (ኢትዮጵያ)
    >>> print(language_name(languageId="gl_ES.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Galego (España)
    >>> print(language_name(languageId="gu_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ગુજરાતી (ભારત)
    >>> print(language_name(languageId="gv_GB.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Gaelg (Rywvaneth Unys)
    >>> print(language_name(languageId="ha_NG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Hausa (Najeriya)
    >>> print(language_name(languageId="hak_TW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    客家話 (中華民國)
    >>> print(language_name(languageId="he_IL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    עברית (ישראל)
    >>> print(language_name(languageId="hi_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    हिन्दी (भारत)
    >>> print(language_name(languageId="hif_FJ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    हिन्दी (Fiji)
    >>> print(language_name(languageId="hne_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    छत्तीसगढ़ी (भारत)
    >>> print(language_name(languageId="hr_HR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Hrvatski (Hrvatska)
    >>> print(language_name(languageId="hsb_DE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Hornjoserbšćina (Němska)
    >>> print(language_name(languageId="ht_HT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kreyòl ayisyen (Ayiti)
    >>> print(language_name(languageId="hu_HU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Magyar (Magyarország)
    >>> print(language_name(languageId="hy_AM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Հայերեն (Հայաստան)
    >>> print(language_name(languageId="ia_FR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Interlingua (Francia)
    >>> print(language_name(languageId="id_ID.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Indonesia (Indonesia)
    >>> print(language_name(languageId="ig_NG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Igbo (Naịjịrịa)
    >>> print(language_name(languageId="ik_CA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Iñupiatun (Kanada)
    >>> print(language_name(languageId="is_IS.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Íslenska (Ísland)
    >>> print(language_name(languageId="it_CH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Italiano (Svizzera)
    >>> print(language_name(languageId="it_IT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Italiano (Italia)
    >>> print(language_name(languageId="iu_CA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ᐃᓄᒃᑎᑐᑦ (ᑲᓇᑕ)
    >>> print(language_name(languageId="ja_JP.utf8")) # doctest: +NORMALIZE_WHITESPACE
    日本語 (日本)
    >>> print(language_name(languageId="ka_GE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ქართული (საქართველო)
    >>> print(language_name(languageId="kab_DZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Taqbaylit (Lezzayer)
    >>> print(language_name(languageId="kk_KZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Қазақ тілі (Қазақстан)
    >>> print(language_name(languageId="kl_GL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kalaallisut (Kalaallit Nunaat)
    >>> print(language_name(languageId="km_KH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ខ្មែរ (កម្ពុជា)
    >>> print(language_name(languageId="kn_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ಕನ್ನಡ (ಭಾರತ)
    >>> print(language_name(languageId="ko_KR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    한국어 (대한민국)
    >>> print(language_name(languageId="kok_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    कोंकणी (भारत)
    >>> print(language_name(languageId="ks_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    کٲشُر (ہِندوستان)
    >>> print(language_name(languageId="ks_IN.utf8@devanagari")) # doctest: +NORMALIZE_WHITESPACE
    कॉशुर (भारत)
    >>> print(language_name(languageId="ku_TR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kurdî (Tirkiye)
    >>> print(language_name(languageId="kw_GB.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kernewek (Rywvaneth Unys)
    >>> print(language_name(languageId="ky_KG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Кыргызча (Кыргызстан)
    >>> print(language_name(languageId="lb_LU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lëtzebuergesch (Lëtzebuerg)
    >>> print(language_name(languageId="lg_UG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Luganda (Yuganda)
    >>> print(language_name(languageId="li_BE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lèmbörgs ('t Belsj)
    >>> print(language_name(languageId="li_NL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lèmbörgs (Nederlands)
    >>> print(language_name(languageId="lij_IT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lìgure (Italia)
    >>> print(language_name(languageId="ln_CD.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lingála (Republíki ya Kongó Demokratíki)
    >>> print(language_name(languageId="lo_LA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ລາວ (ລາວ)
    >>> print(language_name(languageId="lt_LT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lietuvių (Lietuva)
    >>> print(language_name(languageId="lv_LV.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Latviešu (Latvija)
    >>> print(language_name(languageId="lzh_TW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    漢語文言 (Taiwan)
    >>> print(language_name(languageId="mag_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    मगही (भारत)
    >>> print(language_name(languageId="mai_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    मैथिली (भारत)
    >>> print(language_name(languageId="mai_NP.utf8")) # doctest: +NORMALIZE_WHITESPACE
    मैथिली (नेपाल)
    >>> print(language_name(languageId="mfe_MU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kreol morisien (Moris)
    >>> print(language_name(languageId="mg_MG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Malagasy (Madagasikara)
    >>> print(language_name(languageId="mhr_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Марий йылме (Russia)
    >>> print(language_name(languageId="mi_NZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Te reo Māori (Aotearoa)
    >>> print(language_name(languageId="miq_NI.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Mískitu (Nicaragua)
    >>> print(language_name(languageId="mjw_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Karbi (Bhorot)
    >>> print(language_name(languageId="mk_MK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Македонски (Северна Македонија)
    >>> print(language_name(languageId="ml_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    മലയാളം (ഇന്ത്യ)
    >>> print(language_name(languageId="mn_MN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Монгол (Монгол)
    >>> print(language_name(languageId="mni_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    মৈতৈলোন্ (ইন্দিয়া)
    >>> print(language_name(languageId="mnw_MM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    မန် (ဗၟာ)
    >>> print(language_name(languageId="mr_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    मराठी (भारत)
    >>> print(language_name(languageId="ms_MY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Melayu (Malaysia)
    >>> print(language_name(languageId="mt_MT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Malti (Malta)
    >>> print(language_name(languageId="my_MM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    မြန်မာ (မြန်မာ)
    >>> print(language_name(languageId="nan_TW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    閩南語 (中華民國)
    >>> print(language_name(languageId="nan_TW.utf8@latin")) # doctest: +NORMALIZE_WHITESPACE
    Bân-lâm-gú (Tâi-oân)
    >>> print(language_name(languageId="nb_NO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Norsk bokmål (Norge)
    >>> print(language_name(languageId="nds_DE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Neddersass’sch (Düütschland)
    >>> print(language_name(languageId="nds_NL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Neddersass’sch (Nedderlannen)
    >>> print(language_name(languageId="ne_NP.utf8")) # doctest: +NORMALIZE_WHITESPACE
    नेपाली (नेपाल)
    >>> print(language_name(languageId="nhn_MX.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Tlahco nāhuatlahtōlli (Mexihco)
    >>> print(language_name(languageId="niu_NU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ko e vagahau Niuē (Niuē)
    >>> print(language_name(languageId="niu_NZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ko e vagahau Niuē (New Zealand)
    >>> print(language_name(languageId="nl_AW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Nederlands (Aruba)
    >>> print(language_name(languageId="nl_BE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Nederlands (België)
    >>> print(language_name(languageId="nl_NL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Nederlands (Nederland)
    >>> print(language_name(languageId="nn_NO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Norsk nynorsk (Noreg)
    >>> print(language_name(languageId="nr_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    isiNdebele (iSewula Afrika)
    >>> print(language_name(languageId="nso_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Sesotho sa Leboa (Afrika Borwa)
    >>> print(language_name(languageId="oc_FR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Occitan (França)
    >>> print(language_name(languageId="om_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Oromoo (Itoophiyaa)
    >>> print(language_name(languageId="om_KE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Oromoo (Keeniyaa)
    >>> print(language_name(languageId="or_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ଓଡ଼ିଆ (ଭାରତ)
    >>> print(language_name(languageId="os_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ирон (Уӕрӕсе)
    >>> print(language_name(languageId="pa_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ਪੰਜਾਬੀ (ਭਾਰਤ)
    >>> print(language_name(languageId="pa_PK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    پنجابی (پکستان)
    >>> print(language_name(languageId="pap_AW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Papiamento (Aruba)
    >>> print(language_name(languageId="pap_CW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Papiamento (Kòrsou)
    >>> print(language_name(languageId="pl_PL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Polski (Polska)
    >>> print(language_name(languageId="ps_AF.utf8")) # doctest: +NORMALIZE_WHITESPACE
    پښتو (افغانستان)
    >>> print(language_name(languageId="pt_BR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Português (Brasil)
    >>> print(language_name(languageId="pt_PT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Português (Portugal)
    >>> print(language_name(languageId="quz_PE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Qusqu runasimi (Peru)
    >>> print(language_name(languageId="raj_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    राजस्थानी (भारत)
    >>> print(language_name(languageId="ro_RO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Română (România)
    >>> print(language_name(languageId="ru_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Русский (Россия)
    >>> print(language_name(languageId="ru_UA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Русский (Украина)
    >>> print(language_name(languageId="rw_RW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kinyarwanda (U Rwanda)
    >>> print(language_name(languageId="sa_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    संस्कृत भाषा (भारतः)
    >>> print(language_name(languageId="sah_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Саха тыла (Арассыыйа)
    >>> print(language_name(languageId="sat_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ᱥᱟᱱᱛᱟᱲᱤ (ᱤᱱᱰᱤᱭᱟ)
    >>> print(language_name(languageId="sc_IT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Sardu (Itàlia)
    >>> print(language_name(languageId="sd_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    سنڌي (ڀارت)
    >>> print(language_name(languageId="sd_IN.utf8@devanagari")) # doctest: +NORMALIZE_WHITESPACE
    सिन्धी (भारत)
    >>> print(language_name(languageId="se_NO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Davvisámegiella (Norga)
    >>> print(language_name(languageId="sgs_LT.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Žemaitėškā (Lietova)
    >>> print(language_name(languageId="shn_MM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    လိၵ်ႈတႆး (မိူင်းမၢၼ်ႈ)
    >>> print(language_name(languageId="shs_CA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Secwepemctsín (Canada)
    >>> print(language_name(languageId="si_LK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    සිංහල (ශ්‍රී ලංකාව)
    >>> print(language_name(languageId="sid_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Sidaamu Afo (Itiyoophiya)
    >>> print(language_name(languageId="sk_SK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Slovenčina (Slovensko)
    >>> print(language_name(languageId="sl_SI.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Slovenščina (Slovenija)
    >>> print(language_name(languageId="sm_WS.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Gagana faʻa Sāmoa (Sāmoa)
    >>> print(language_name(languageId="so_DJ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Soomaali (Jabuuti)
    >>> print(language_name(languageId="so_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Soomaali (Itoobiya)
    >>> print(language_name(languageId="so_KE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Soomaali (Kenya)
    >>> print(language_name(languageId="so_SO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Soomaali (Soomaaliya)
    >>> print(language_name(languageId="sq_AL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Shqip (Shqipëri)
    >>> print(language_name(languageId="sq_MK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Shqip (Maqedonia e Veriut)
    >>> print(language_name(languageId="sr_ME.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Српски (Црна Гора)
    >>> print(language_name(languageId="sr_RS.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Српски (Србија)
    >>> print(language_name(languageId="sr_RS.utf8@latin")) # doctest: +NORMALIZE_WHITESPACE
    Srpski (Latinica) (Srbija)
    >>> print(language_name(languageId="ss_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    siSwati (iNingizimu Afrika)
    >>> print(language_name(languageId="st_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Sesotho (Afrika Borwa)
    >>> print(language_name(languageId="sv_FI.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Svenska (Finland)
    >>> print(language_name(languageId="sv_SE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Svenska (Sverige)
    >>> print(language_name(languageId="sw_KE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kiswahili (Kenya)
    >>> print(language_name(languageId="sw_TZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Kiswahili (Tanzania)
    >>> print(language_name(languageId="szl_PL.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Ślōnskŏ gŏdka (Polska)
    >>> print(language_name(languageId="ta_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    தமிழ் (இந்தியா)
    >>> print(language_name(languageId="ta_LK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    தமிழ் (இலங்கை)
    >>> print(language_name(languageId="tcy_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ತುಳು (ಭಾರತ)
    >>> print(language_name(languageId="te_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    తెలుగు (భారతదేశం)
    >>> print(language_name(languageId="tg_TJ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Тоҷикӣ (Тоҷикистон)
    >>> print(language_name(languageId="th_TH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ไทย (ไทย)
    >>> print(language_name(languageId="the_NP.utf8")) # doctest: +NORMALIZE_WHITESPACE
    थारु (नेपाल)
    >>> print(language_name(languageId="ti_ER.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ትግርኛ (ኤርትራ)
    >>> print(language_name(languageId="ti_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ትግርኛ (ኢትዮጵያ)
    >>> print(language_name(languageId="tig_ER.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ትግረ (ኤርትራ)
    >>> print(language_name(languageId="tk_TM.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Türkmen dili (Türkmenistan)
    >>> print(language_name(languageId="tl_PH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Tagalog (Pilipinas)
    >>> print(language_name(languageId="tn_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Setswana (Aforika Borwa)
    >>> print(language_name(languageId="to_TO.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lea fakatonga (Tonga)
    >>> print(language_name(languageId="tpi_PG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Tok Pisin (Papua Niugini)
    >>> print(language_name(languageId="tr_CY.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Türkçe (Kıbrıs)
    >>> print(language_name(languageId="tr_TR.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Türkçe (Türkiye)
    >>> print(language_name(languageId="ts_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Xitsonga (Afrika Dzonga)
    >>> print(language_name(languageId="tt_RU.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Татар (Россия)
    >>> print(language_name(languageId="tt_RU.utf8@iqtelif")) # doctest: +NORMALIZE_WHITESPACE
    Tatar tele (Urıs Patşahlıq)
    >>> print(language_name(languageId="ug_CN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ئۇيغۇرچە (جۇڭگو)
    >>> print(language_name(languageId="uk_UA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Українська (Україна)
    >>> print(language_name(languageId="unm_US.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Lenape (United States)
    >>> print(language_name(languageId="ur_IN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    اردو (بھارت)
    >>> print(language_name(languageId="ur_PK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    اردو (پاکستان)
    >>> print(language_name(languageId="uz_UZ.utf8")) # doctest: +NORMALIZE_WHITESPACE
    O‘zbek (Oʻzbekiston)
    >>> print(language_name(languageId="uz_UZ.utf8@cyrillic")) # doctest: +NORMALIZE_WHITESPACE
    Ўзбекча (Ўзбекистон)
    >>> print(language_name(languageId="ve_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Tshivenḓa (Afurika  Tshipembe)
    >>> print(language_name(languageId="vi_VN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Tiếng Việt (Việt Nam)
    >>> print(language_name(languageId="wa_BE.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Walon (Beldjike)
    >>> print(language_name(languageId="wae_CH.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Walser (Schwiz)
    >>> print(language_name(languageId="wal_ET.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ወላይታቱ (ኢትዮጵያ)
    >>> print(language_name(languageId="wo_SN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Wolof (Senegaal)
    >>> print(language_name(languageId="xh_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    isiXhosa (eMzantsi Afrika)
    >>> print(language_name(languageId="yi_US.utf8")) # doctest: +NORMALIZE_WHITESPACE
    ייִדיש (פֿאַראייניגטע שטאַטן)
    >>> print(language_name(languageId="yo_NG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Èdè Yorùbá (Nàìjíríà)
    >>> print(language_name(languageId="yue_HK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    粵語 (中華人民共和國香港特別行政區)
    >>> print(language_name(languageId="yuw_PG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    Uruwa (Papua New Guinea)
    >>> print(language_name(languageId="zh_CN.utf8")) # doctest: +NORMALIZE_WHITESPACE
    简体中文 (中国)
    >>> print(language_name(languageId="zh_HK.utf8")) # doctest: +NORMALIZE_WHITESPACE
    繁體中文 (中華人民共和國香港特別行政區)
    >>> print(language_name(languageId="zh_SG.utf8")) # doctest: +NORMALIZE_WHITESPACE
    简体中文 (新加坡)
    >>> print(language_name(languageId="zh_TW.utf8")) # doctest: +NORMALIZE_WHITESPACE
    繁體中文 (台灣)
    >>> print(language_name(languageId="zu_ZA.utf8")) # doctest: +NORMALIZE_WHITESPACE
    isiZulu (iNingizimu Afrika)

    ######################################################################
    >>> print(territory_name(territoryId="001", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
    World

    >>> print(territory_name(territoryId="001", languageIdQuery="nl")) # doctest: +NORMALIZE_WHITESPACE
    Wereld

    >>> print(territory_name(territoryId="AE", languageIdQuery="ar")) # doctest: +NORMALIZE_WHITESPACE
        الإمارات العربية المتحدة

    >>> print(territory_name(territoryId="AE", languageIdQuery="de")) # doctest: +NORMALIZE_WHITESPACE
        Vereinigte Arabische Emirate

    >>> print(territory_name(territoryId="AE", languageIdQuery="en")) # doctest: +NORMALIZE_WHITESPACE
        United Arab Emirates

    >>> print(territory_name(territoryId="AE", languageIdQuery=None)) # doctest: +NORMALIZE_WHITESPACE
    United Arab Emirates

    >>> print(territory_name(territoryId="AE", languageIdQuery=None, fallback=False)) # doctest: +NORMALIZE_WHITESPACE

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

    >>> languageId("Shuswap")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("Shuswap")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("shuswap")  # doctest: +NORMALIZE_WHITESPACE
        'shs'

    >>> languageId("sHuSwAp")  # doctest: +NORMALIZE_WHITESPACE
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
    >>> print(list_common_keyboards())  # doctest: +NORMALIZE_WHITESPACE
        ['af(ps)', 'al', 'am', 'ara', 'az', 'ba', 'be(oss)', 'bg', 'br', 'bt', 'by', 'ca(eng)', 'ca(ike)', 'ch', 'cn', 'cn(ug)', 'cz', 'de(nodeadkeys)', 'dk', 'ee', 'es', 'es(ast)', 'es(cat)', 'et', 'fi', 'fo', 'fr(bre)', 'fr(oss)', 'gb', 'ge', 'gr', 'hr', 'hu', 'ie(CloGaelach)', 'il', 'in(eng)', 'ir', 'is', 'it', 'jp', 'ke', 'kg', 'kh', 'kr', 'kz', 'la', 'latam', 'lt', 'lv', 'ma(tifinagh)', 'mk', 'mm', 'mn', 'mt', 'mv', 'ng(hausa)', 'ng(igbo)', 'ng(yoruba)', 'no', 'np', 'ph', 'pk', 'pl', 'ro', 'rs', 'rs(latin)', 'ru', 'ru(bak)', 'ru(chm)', 'ru(cv)', 'ru(kom)', 'ru(os_winkeys)', 'ru(sah)', 'ru(tt)', 'ru(udm)', 'ru(xal)', 'se', 'si', 'sk', 'sn', 'syc', 'th', 'tj', 'tm', 'tr', 'tr(crh)', 'tr(ku)', 'tw', 'ua', 'us', 'us(altgr-intl)', 'us(euro)', 'us(intl)', 'uz', 'vn', 'za']
    >>> print(list_common_keyboards(languageId='fr'))  # doctest: +NORMALIZE_WHITESPACE
        ['fr(oss)']
    >>> print(list_common_keyboards(territoryId='CA'))   # doctest: +NORMALIZE_WHITESPACE
        ['ca(eng)']
    >>> print(list_common_keyboards(territoryId='FR'))   # doctest: +NORMALIZE_WHITESPACE
        ['fr(oss)']
    >>> print(list_common_keyboards(languageId='fr', territoryId='CA'))   # doctest: +NORMALIZE_WHITESPACE
        ['ca']
    >>> print(list_common_keyboards(languageId='de', territoryId='FR'))   # doctest: +NORMALIZE_WHITESPACE
        ['fr(oss)']
    >>> print(list_common_keyboards(languageId='sr', scriptId='Latn'))   # doctest: +NORMALIZE_WHITESPACE
        ['rs(latin)']
    >>> print(list_common_keyboards(languageId='zh', scriptId='Hans'))   # doctest: +NORMALIZE_WHITESPACE
        ['cn']
    >>> print(list_common_keyboards(languageId='zh', scriptId='Hans', territoryId='TW'))   # doctest: +NORMALIZE_WHITESPACE
        ['tw']
    >>> print(list_common_languages())   # doctest: +NORMALIZE_WHITESPACE
        ['ar', 'en', 'fr', 'de', 'ja', 'zh', 'ru', 'es']
    '''


if __name__ == "__main__":
    import doctest
    (FAILED, ATTEMPTED) = doctest.testmod()
    if FAILED:
        # Return number of failed tests:
        sys.exit(FAILED)
    sys.exit(0)
