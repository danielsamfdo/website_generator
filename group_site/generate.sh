#!/bin/bash

TITLE_PREFIX="ANSR " 

STUDENTS_CONTENT="students_content.html"
CV_CONTENT="bio_content.txt"
PUB_CONTENT="year_publications.html"
PROJ_CONTENT="projects_content.txt"
ABOUT_CONTENT="about_content.txt"
JOB_CONTENT="jobs_content.txt"
NEWS_CONTENT="news_content.html"

# Array pretending to be a Pythonic dictionary
ARRAY=( "home:$ABOUT_CONTENT"
        "publications:$PUB_CONTENT"
        "projects:$PROJ_CONTENT"
        "people:$STUDENTS_CONTENT"
        "jobs:$JOB_CONTENT"
        "news:$NEWS_CONTENT"
      )

HEADERFILESNAMES=( "home:Home"
        "publications:Publications"
        "projects:Projects"
        "people:People"
        "jobs:Jobs"
        "news:News"
      )

HEADERURLS=( "home:index.html"
        "publications:publications.html"
        "projects:projects.html"
        "people:people.html"
        "jobs:jobs.html"
        "news:news.html"
      )

template2 () {
  printf "<!DOCTYPE html><html lang='en'><head><title>"
  printf "$4"
  echo $(cat temp3_2.html)
  echo "$2"
  echo $(cat temp3_3.html)
  echo "$3"
  echo $(cat temp3_4.html) 
}


template1 () {
  printf "<html><head><script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script><script src='js/script.js'></script><link rel='stylesheet' type='text/css' href='style.css'><title>"
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
    template2 "$top_content" "$nav_content" "$(cat $INNER_CONTENT)" "$title_value" > $URL_FILE_NAME
  done
  zip -r group_site.zip images/ css/ js/ index.html publications.html projects.html people.html jobs.html news.html style.css temp3_css.css *.js
}

generate_single_webpage (){
  template="temp3.html"
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

