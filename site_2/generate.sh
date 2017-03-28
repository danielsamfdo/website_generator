#!/bin/bash
 

TITLE_PREFIX="Prof.Arun " 
STUDENTS_CONTENT="students_content.txt"
CV_CONTENT="bio_content.txt"
PUB_CONTENT="publications_content.html"
RES_CONTENT="research_content.txt"
ABOUT_CONTENT="about_content.txt"
CONTACT_CONTENT="contact_content.txt"
# Array pretending to be a Pythonic dictionary
ARRAY=( "about:$ABOUT_CONTENT"
        "research:$RES_CONTENT"
        "publications:$PUB_CONTENT"
        "cv:$CV_CONTENT"
        "students:$STUDENTS_CONTENT"
        "contact:$CONTACT_CONTENT"
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





navigation_content () {
  for i in "${!HEADERFILESNAMES[@]}" ; do
    header="${HEADERFILESNAMES[$i]}"
    header_url="${HEADERURLS[$i]}" 
    URL_LOCATION="${header_url##*:}"
    URL_NAME="${header##*:}"
    printf "<li><a href='$URL_LOCATION'>$URL_NAME</a></li>"
  done
}

generate_entire_website (){
  template="temp3.html"
  side_content=$(cat side_content.txt)
  nav_content=$(navigation_content)
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
      template2 "$side_content" "$nav_content" "$(cat $INNER_CONTENT)" "$title_value" > $URL_FILE_NAME
  done
  zip -r personal_site.zip assets/ *.html *.css *.js
}

generate_single_webpage (){
  template="temp3.html"
  side_content=$(cat side_content.txt)
  nav_content=$(navigation_content)
  for i in "${!ARRAY[@]}" ; do
    header="${ARRAY[$i]}"
    title_value=$TITLE_PREFIX
    title="${HEADERFILESNAMES[$i]}"
    title="${title##*:}"
    title_value+=$title
    url_file="${HEADERURLS[$i]}"
    URL_FILE_NAME="${url_file##*:}"
    INNER_CONTENT="${header##*:}"
    if [ "$INNER_CONTENT" == "$1" ]; then
      echo "GENERATING CONTENT using $INNER_CONTENT"
      template2 "$side_content" "$nav_content" "$(cat $INNER_CONTENT)" "$title_value" > $URL_FILE_NAME
    fi
  done 
}


while getopts ":a:b:" opt; do
  case $opt in
    a)
      echo "-a was triggered, Parameter: $OPTARG $3 $4" >&2
      generate_single_webpage $3
      ;;
    b)
      generate_entire_website
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
