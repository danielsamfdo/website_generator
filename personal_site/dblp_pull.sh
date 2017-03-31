#!/bin/bash 
# Content of dblp_script.sh
wget -O dblp_page.html http://dblp.uni-trier.de/pers/hd/v/Venkataramani:Arun
grep -o 'http://dblp.uni-trier.de/rec/bibtex[^"]*' dblp_page.html > dblp_urls.txt
wget -i dblp_urls.txt -O dblp_tmp.html
html2text dblp_tmp.html > dblp_tmp.bib
r="0"
while IFS='' read -r line; do
 head=${line:0:1}
 if [ "$head" == "@" ]; then
  r="1"
 fi
 if [ "$r" == "1" ]; then
       printf "%s\n" "$line"
 fi
 if [ "$head" == "}" ]; then
  r="0"
 fi
done < dblp_tmp.bib > dblp.bib