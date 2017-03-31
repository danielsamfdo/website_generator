import csv
from collections import OrderedDict
import sys
import re

def change_to_html_characters(string_content):
  string_content = string_content.replace("<","&lt;")
  string_content = string_content.replace(">","&gt;")
  return string_content

def generate_students_page(file_name):
  studentReader = csv.reader(open('Students.txt', 'rb'), delimiter=',', skipinitialspace=True)
  data = OrderedDict()
  keys = []
  for row in studentReader:
    if(row[0] in data):
      data[row[0]].append(row[1:])
    else:
      data.update({row[0]: [row[1:]]})

  target = open(file_name, 'w')
  for key in data:
    if(len(key)>0):
      content = "<h4>%s</h4><div class=\"row\">" %(key)
      for item in data[key]:
          url_present = True if len(item[2])>0 else False
          img = item[1] if len(item[1])>0 else "assets/img/profpic_man.jpg"
          img_tag = "<img class=\"img-circle student_image\" src=\"%s\">"%(img)
          assert len(item[0])>0
          name = "<a href='%s'>%s</a>"%(item[2], item[0]) if(url_present) else item[0]
          name_tag = "<span>%s</span>"%(name)
          entry = img_tag + name_tag
          content += "<div class='col-md-3 m-b-10'>%s</div>" %(entry)
      content+= "</div>"
      target.write(content)
  print("Generated File in %s"%(file_name))
  target.close()

def generate_contact_page(file_name):
  source_file = 'Contact.txt'
  source = open(source_file, 'rb')
  target = open(file_name, 'w')
  content = ""
  for line in source.readlines():
    # line_content = change_to_html_characters(line)
    content += "<p align='justify'>%s</p>"%(line)
  target.write(content)
  print("Generated File in %s"%(file_name))
  target.close()
  source.close()


def generate_bio_page(file_name):
  source_file = 'Bio.txt'
  
  source = open(source_file, 'rb')
  target = open(file_name, 'w')
  file_lines = source.readlines()
  section_header = file_lines[0]
  content = "<h4>%s</h4>"%(section_header)
  
  assert len(file_lines)>2
  cv_link = "<a class='waves-effect waves-teal btn-flat pull-right m-b-15' href='%s' target='_blank'>Detailed CV</a>"%(file_lines[1])

  for line in file_lines[2:]:
    # line_content = change_to_html_characters(line)
    content += "<p align='justify'>%s</p>"%(line)
  content += cv_link
  target.write(content)
  print("Generated File in %s"%(file_name))
  target.close()
  source.close()

def generate_about_page(file_name):
  source_file = 'About.txt'
  source = open(source_file, 'rb')
  target = open(file_name, 'w')
  file_lines = source.readlines()
  section_header = file_lines[0]
  content = "<h4>%s</h4>"%(section_header)
  
  assert len(file_lines)>2
  cv_link = "<a class='waves-effect waves-teal btn-flat pull-right m-b-15' href='%s' target='_blank'>Detailed CV</a>"%(file_lines[1])

  for line in file_lines[2:]:
    # line_content = change_to_html_characters(line)
    content += "<p align='justify'>%s</p>"%(line)
  content += cv_link
  target.write(content)
  print("Generated File in %s"%(file_name))
  target.close()
  source.close()
  
def main():
  if(sys.argv[1] == "students"):
    generate_students_page("students_content.html")
  elif(sys.argv[1] == "contact"):
    generate_contact_page("contact_content.html")
  elif(sys.argv[1] == "bio"):
    generate_bio_page("bio_content.html")
  elif(sys.argv[1] == "home"):
    generate_about_page("about_content.html")
  else:
    print "UNKNOWN OPTION USED"

if __name__ == "__main__":
  main()