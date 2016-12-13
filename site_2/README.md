There are three main scripts:

1) dblp_pull.sh : Which pulls all the dblp publications from the user profile page.

2) generate_publications_content.py : 
    Inside the above file if you require to do a fresh pull from google scholar and then generate publications contents, Uncomment the line 483(save_publications_from_google_scholar()). This script generates the file for publications_content in publications_content.html

3) generate.sh: This script generates the website,  The parameters that can be added are
    
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