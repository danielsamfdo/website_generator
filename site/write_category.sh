#!/bin/bash 

# GET ONE BIB FILE
# REMOVE DUPLICATE ENTRIES
# ENTER CATEGORIES
echo "" > tmp_main_bib.bib
# sed -i "" -e $"s/^}$/,catteggory = 'SELECT Network'\\n}/g" dup_dblp.bib
# perl -pe 's/^}/\tcatteggory = testssdsf,\n}/g' dup_dblp.bib | perl -pe 's/.+*[^,]$/"\tcatteggory = testssdsf,\n}"/g'
python process_dblp.py
cat main_dblp.bib >> tmp_main_bib.bib
cat mypubs.bib >> tmp_main_bib.bib
cat tmp_main_bib > main.bib

