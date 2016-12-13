#!/bin/bash

TITLE_PREFIX="ANSR " 

# Array pretending to be a Pythonic dictionary
ARRAY=( "home:home_content.html"
        "publications:publications_content.html"
        "projects:projects_content.html"
        "people:people_content.html"
        "jobs:jobs_content.html"
        "news:news_content.html"
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


top_content=$(cat top_content.txt)


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
    template2 "$top_content" "$nav_content" "$(cat $INNER_CONTENT)" "$title_value" > $URL_FILE_NAME
done
