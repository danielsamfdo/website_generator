#!/bin/bash

TITLE_PREFIX="Prof.Arun " 

# Array pretending to be a Pythonic dictionary
ARRAY=( "about:1_test.txt"
        "cv:2_test.txt"
        "publications:select_new.html"
      )

HEADERFILESNAMES=( "about:Home"
        "cv:Bio"
        "publications:Publications &amp; Projects"
      )

HEADERURLS=( "about:index.html"
        "cv:cv.html"
        "publications:publications.html"
      )

template1 () {
  printf "<html><head><link rel='stylesheet' type='text/css' href='style.css'><title>"
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
