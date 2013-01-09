#!/bin/bash
#
# Shell script to manage locales, languages, .po files...
#
# Run this file in your product folder
# E.g. : in yourproduct.name/yourproduct/name
#

CATALOGNAME="collective.dms.basecontent"

# List of managed languages (separated by space)
# Ex LANGUAGES="fr|French|fr-fr;fr-be;fr-ca nl|Dutch|nl-be;nl-nl"
LANGUAGES="en|English|en-au;en-ca;en-gb;en-us fr|French|fr-fr;fr-be;fr-ca nl|Dutch|nl-be;nl-nl"

# Create locales folder structure for languages
install -d locales

# Rebuild .pot
if ! test -f locales/$CATALOGNAME.pot || [ "$1" == "rebuild" ]; then
    echo "Rebuilding locales/$CATALOGNAME.pot"
    i18ndude rebuild-pot --pot locales/$CATALOGNAME.pot --create $CATALOGNAME .
fi

# Finding pot files
for pot in $(find locales -mindepth 1 -maxdepth 1 -type f -name "*.pot" ! -name generated.pot); do
    #finding pot basename as catalog
    catalog=`basename $pot .pot`
    echo "=> Found pot $pot"
    # First initialization of po files with base languages if po doesn't exist
    for language in $LANGUAGES; do
        arr=(`echo $language | cut -d "|"  --output-delimiter=" " -f 1-`)
        langcode=${arr[0]}
        install -d locales/$langcode/LC_MESSAGES

        PO=locales/$langcode/LC_MESSAGES/$catalog.po
        # Create po file if not exists and modify header
        if ! test -f $PO; then
            touch $PO
            echo " -> Syncing $PO"
            i18ndude sync --pot $pot $PO
            sed -i -e "/^\\\"Domain: DOMAIN/ s/DOMAIN/$catalog/" $PO
            sed -i -e "/^\\\"Language-Code: en/ s/en/$langcode/" $PO
            langname=${arr[1]}
            if [ -n "$langname" ]; then
                sed -i -e "/^\\\"Language-Name: English/ s/English/$langname/" $PO
            fi
            fallbackstr=${arr[2]}
            if [ -n "$fallbackstr" ]; then
                fallbacklist=`echo $fallbackstr | cut -d ";"  --output-delimiter=" " -f 1-`
                echo $fallbacklist
                sed -i -e "/^\\\"Language-Name:/ a\"X-is-fallback-for: $fallbacklist\\\n\"" $PO
            fi
        fi
    done
    # Sync po files
    for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
        if test -d $lang/LC_MESSAGES; then
            PO=$lang/LC_MESSAGES/$catalog.po
            # Sync po file
            echo " -> Syncing $PO"
            i18ndude sync --pot $pot $PO

            # Compile .po to .mo
            MO=$lang/LC_MESSAGES/$catalog.mo
            #echo " -> Compiling $MO"
            #msgfmt -o $MO $lang/LC_MESSAGES/$catalog.po
        fi
    done
done