#!/bin/bash

TITLE_PREFIX="Prof.Arun " 

# Array pretending to be a Pythonic dictionary
ARRAY=( "about:about_content.txt"
        "research:research_content.txt"
        "publications:publications_content.html"
        "cv:cv_content.txt"
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

template2 () {
  echo $(cat template_1.html)
  echo "$4"
  echo $(cat template_2.html)
  echo "$2"
  echo $(cat template_3.html)
  echo "$1"
  echo $(cat template_4.html)
  echo "$3"
  echo $(cat template_5.html) 
}


template1 () {
  printf "<html><head><script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script><link rel='stylesheet' type='text/css' href='style.css'><script src='temp3_js.js'></script><title>"
  echo "$4"
  printf "</title></head><body><div class='box'>"
  printf "%s", "$1"
  printf "<div id='navigation'>"
  echo "$2"
  printf "</div><div class='innerbox'>"
  echo "$3"
  printf "</div></div></body></html>" 
}


side_content=$(cat side_content.txt)


navigation_content () {
  for i in "${!HEADERFILESNAMES[@]}" ; do
    header="${HEADERFILESNAMES[$i]}"
    header_url="${HEADERURLS[$i]}" 
    URL_LOCATION="${header_url##*:}"
    URL_NAME="${header##*:}"
    printf "<li><a href='$URL_LOCATION'>$URL_NAME</a></li>"
  done
}
template="temp3.html"

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
    # sed -e "s/{{NAV_CONTENT}}/$nav_content/g" $template > tmp.html
    # r=$(printf "%q", $(cat $INNER_CONTENT))
    # sed -e "s/{{INNER_CONTENT}}/$r/g" tmp.html > tmp2.html
    # sed -e "s/{{TITLE}}/$title_value/g" tmp2.html > $URL_FILE_NAME
    template2 "$side_content" "$nav_content" "$(cat $INNER_CONTENT)" "$title_value" > $URL_FILE_NAME
done
