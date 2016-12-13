#!/bin/bash

TITLE_PREFIX="Prof.Arun " 

# Array pretending to be a Pythonic dictionary
ARRAY=( "about:1_test.txt"
        "research:research_content.txt"
        "publications:select_new.html"
        "cv:2_test.txt"
        "students:students_content.txt"
        "contact:contact_content.txt"
      )

HEADERFILESNAMES=( "about:Home"
        "research:Research"
        "publications:Publications &amp; Projects"
        "cv:Bio"
        "students:Students"
        "contact:Contact"
      )

HEADERURLS=( "about:index.html"
        "research:research.html"
        "publications:publications.html"
        "cv:cv.html"
        "students:students.html"
        "contact:contact.html"
      )

template1 () {
  printf "<html><head><meta charset='ISO-8859-1'><meta charset='utf-8'><meta http-equiv='content-type' content='text/html; charset=UTF-8' /><link rel='stylesheet' type='text/css' href='style.css'><script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script><script src='script.js'></script><title>"
  printf "$4"
  printf "</title></head><body><div class='box'>"
  printf "%s", "$1"
  printf "<div id='navigation'>"
  echo "$2"
  printf "</div><div class='innerbox'>"
  echo "$3"
  printf "</div></div></body></html>" 
}

top_content=$(cat top_content.txt)


navigation_content () {
  for i in "${!HEADERFILESNAMES[@]}" ; do
    header="${HEADERFILESNAMES[$i]}"
    header_url="${HEADERURLS[$i]}" 
    URL_LOCATION="${header_url##*:}"
    URL_NAME="${header##*:}"
    printf "<a href='$URL_LOCATION'>$URL_NAME</a>"
  done
}

nav_content=$(navigation_content)
echo $nav_content
for i in "${!ARRAY[@]}" ; do
    header="${ARRAY[$i]}"
    title_value=$TITLE_PREFIX
    title="${HEADERFILESNAMES[$i]}"
    title="${title##*:}"
    title_value+=$title
    echo $title_value
    url_file="${HEADERURLS[$i]}"
    URL_FILE_NAME="${url_file##*:}"
    INNER_CONTENT="${header##*:}"
    template1 "$top_content" "$nav_content" "$(cat $INNER_CONTENT)" "$title_value" > $URL_FILE_NAME
done
