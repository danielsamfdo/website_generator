generate.sh: This script generates the website,  The parameters that can be added are
    
TITLE_PREFIX="Title  " 

# YOUR CONTENT File Names
# Array pretending to be a Pythonic dictionary
ARRAY=( "about:1_test.txt"
        "research:research_content.txt"
        "publications:select_new.html"
        "cv:2_test.txt"
        "students:students_content.txt"
        "contact:contact_content.txt"
      )


# YOUR HEADER TAB NAMES

HEADERFILESNAMES=( "about:Home"
        "research:Research"
        "publications:Publications &amp; Projects"
        "cv:Bio"
        "students:Students"
        "contact:Contact"
      )


#YOUR HEADER URLS

HEADERURLS=( "about:index.html"
        "research:research.html"
        "publications:publications.html"
        "cv:cv.html"
        "students:students.html"
        "contact:contact.html"
      ) 