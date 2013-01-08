#!/bin/sh
#
# Shell script to manage locales, languages, .po files...
#
# Run this file in your product folder
# E.g. : in yourproduct.name/yourproduct/name
#

CATALOGNAME="collective.dms.basecontent"

# List of managed languages (separated by space)
LANGUAGES="en fr nl"

# Create locales folder structure for languages
install -d locales
for lang in $LANGUAGES; do
    install -d locales/$lang/LC_MESSAGES
done

# Rebuild .pot
if ! test -f locales/$CATALOGNAME.pot; then
    i18ndude rebuild-pot --pot locales/$CATALOGNAME.pot --create $CATALOGNAME .
fi

# Finding pot files
for pot in $(find locales -mindepth 1 -maxdepth 1 -type f -name "*.pot" ! -name generated.pot); do
    catalog=`echo $pot | cut -d "/" -f 2 | cut -d "." -f 1`
    echo "=> Found pot $pot"
    # Compile po files
    for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
    
        if test -d $lang/LC_MESSAGES; then
    
            PO=$lang/LC_MESSAGES/$catalog.po
            # Create po file if not exists
            touch $PO
    
            # Sync po file
            echo " -> Syncing $PO"
            i18ndude sync --pot $pot $PO
    
            # Compile .po to .mo (msgfmt is in package gettext)
            MO=$lang/LC_MESSAGES/$catalog.mo
            echo " -> Compiling $MO"
            msgfmt -o $MO $lang/LC_MESSAGES/$catalog.po
        fi
    done
done