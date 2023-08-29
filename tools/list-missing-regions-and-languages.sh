#!/bin/bash

# list territories which have glibc locales but are not in territories.xml:

echo "----------------------------------------------------------------------"
echo "Missing territories:"
MISSING_TERRITORIES=
MISSING_TERRITORIES_COUNT=0
for i in $(locale -a | grep -a _ | perl -pe 's/.*_([A-Z]{2,2}).*/\1/g' | sort | uniq  ); do grep -q $i territories.xml; if [ $? -eq 1 ]; then MISSING_TERRITORIES="$MISSING_TERRITORIES $i"; MISSING_TERRITORIES_COUNT=$(expr $MISSING_TERRITORIES_COUNT + 1); fi; done
echo $MISSING_TERRITORIES
echo count=$MISSING_TERRITORIES_COUNT

echo "----------------------------------------------------------------------"
echo "Missing languages:"
MISSING_LANGUAGES=
MISSING_LANGUAGES_COUNT=0
for i in $(locale -a | grep -a _ | perl -pe 's/([a-z]{2,3})_.*/\1/g' | sort | uniq  ); do grep -q "<languageId>$i</languageId>" languages.xml; if [ $? -eq 1 ]; then MISSING_LANGUAGES="$MISSING_LANGUAGES $i"; MISSING_LANGUAGES_COUNT=$(expr $MISSING_LANGUAGES_COUNT + 1); fi; done
echo $MISSING_LANGUAGES
echo count=$MISSING_LANGUAGES_COUNT

echo "----------------------------------------------------------------------"
echo "Missing locales in languages.xml:"
MISSING_LOCALES_IN_LANGUAGES=
MISSING_LOCALES_IN_LANGUAGES_COUNT=0
for i in $(locale -a | grep -a utf8 | perl -pe 's/utf8/UTF-8/g' | grep -v C.UTF-8 | sort | uniq  ); do grep -q "<localeId>$i</localeId>" languages.xml; if [ $? -eq 1 ]; then MISSING_LOCALES_IN_LANGUAGES="$MISSING_LOCALES_IN_LANGUAGES $i"; MISSING_LOCALES_IN_LANGUAGES_COUNT=$(expr $MISSING_LOCALES_IN_LANGUAGES_COUNT + 1); fi; done
echo $MISSING_LOCALES_IN_LANGUAGES
echo count=$MISSING_LOCALES_IN_LANGUAGES_COUNT

echo "----------------------------------------------------------------------"
echo "Missing locales in territories.xml:"
MISSING_LOCALES_IN_TERRITORIES=
MISSING_LOCALES_IN_TERRITORIES_COUNT=0
for i in $(locale -a | grep -a utf8 | perl -pe 's/utf8/UTF-8/g' | grep -v '\(C\|eo\|ia_FR\).UTF-8' | sort | uniq  ); do grep -q "<localeId>$i</localeId>" territories.xml; if [ $? -eq 1 ]; then MISSING_LOCALES_IN_TERRITORIES="$MISSING_LOCALES_IN_TERRITORIES $i"; MISSING_LOCALES_IN_TERRITORIES_COUNT=$(expr $MISSING_LOCALES_IN_TERRITORIES_COUNT + 1); fi; done
echo $MISSING_LOCALES_IN_TERRITORIES
echo count=$MISSING_LOCALES_IN_TERRITORIES_COUNT

echo "----------------------------------------------------------------------"
echo "Locales which are in langtable but missing in glibc:"
MISSING_LOCALES_IN_GLIBC=
MISSING_LOCALES_IN_GLIBC_COUNT=0
for i in $(grep "<localeId>.*</localeId>" *.xml | perl -pe 's/.*<localeId>(([a-z]{2,3}_|eo|syr).*)<\/localeId>.*/\1/g')
do
    LC_ALL=$i locale charmap 2>&1 | grep -q UTF-8
    if [ $? -eq 1 ]; then
        MISSING_LOCALES_IN_GLIBC="$MISSING_LOCALES_IN_GLIBC $i"
        MISSING_LOCALES_IN_GLIBC_COUNT=$(expr $MISSING_LOCALES_IN_GLIBC_COUNT + 1)
    fi
done
echo $MISSING_LOCALES_IN_GLIBC
echo count=$MISSING_LOCALES_IN_GLIBC_COUNT
