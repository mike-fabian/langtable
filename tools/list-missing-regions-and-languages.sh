#!/bin/bash

# list territories which have glibc locales but are not in territories.xml:

MISSING_TERRITORIES=
MISSING_TERRITORIES_COUNT=0
for i in $(locale -a | grep _ | perl -pe 's/.*_([A-Z]{2,2}).*/\1/g' | sort | uniq  ); do grep -q $i territories.xml; if [ $? -eq 1 ]; then MISSING_TERRITORIES="$MISSING_TERRITORIES $i"; MISSING_TERRITORIES_COUNT=$(expr $MISSING_TERRITORIES_COUNT + 1); fi; done
echo $MISSING_TERRITORIES
echo count=$MISSING_TERRITORIES_COUNT

MISSING_LANGUAGES=
MISSING_LANGUAGES_COUNT=0
for i in $(locale -a | grep _ | perl -pe 's/([a-z]{2,3})_.*/\1/g' | sort | uniq  ); do grep -q "<languageId>$i</languageId>" languages.xml; if [ $? -eq 1 ]; then MISSING_LANGUAGES="$MISSING_LANGUAGES $i"; MISSING_LANGUAGES_COUNT=$(expr $MISSING_LANGUAGES_COUNT + 1); fi; done
echo $MISSING_LANGUAGES
echo count=$MISSING_LANGUAGES_COUNT


