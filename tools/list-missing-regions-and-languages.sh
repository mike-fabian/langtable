#!/bin/bash

# list countries which have glibc locales but are not in countries.xml:

MISSING_COUNTRIES=
MISSING_COUNTRIES_COUNT=0
for i in $(locale -a | grep _ | perl -pe 's/.*_([A-Z]{2,2}).*/\1/g' | sort | uniq  ); do grep -q $i countries.xml; if [ $? -eq 1 ]; then MISSING_COUNTRIES="$MISSING_COUNTRIES $i"; MISSING_COUNTRIES_COUNT=$(expr $MISSING_COUNTRIES_COUNT + 1); fi; done
echo $MISSING_COUNTRIES
echo count=$MISSING_COUNTRIES_COUNT

MISSING_LANGUAGES=
MISSING_LANGUAGES_COUNT=0
for i in $(locale -a | grep _ | perl -pe 's/([a-z]{2,3})_.*/\1/g' | sort | uniq  ); do grep -q "<languageId>$i</languageId>" languages.xml; if [ $? -eq 1 ]; then MISSING_LANGUAGES="$MISSING_LANGUAGES $i"; MISSING_LANGUAGES_COUNT=$(expr $MISSING_LANGUAGES_COUNT + 1); fi; done
echo $MISSING_LANGUAGES
echo count=$MISSING_LANGUAGES_COUNT


