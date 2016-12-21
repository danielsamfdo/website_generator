import csv
from collections import OrderedDict
from collections import defaultdict
import sys
import re

def change_to_html_characters(string_content):
  string_content = string_content.replace("<","&lt;")
  string_content = string_content.replace(">","&gt;")
  return string_content

def generate_students_page(file_name):
  studentReader = csv.reader(open('Students.txt', 'rb'), delimiter=',', skipinitialspace=True)
  data = OrderedDict()
  for row in studentReader:
    if(row[0] in data):
      data[row[0]].append(row[1:])
    else:
      data.update({row[0]: [row[1:]]})
  # print data
  target = open(file_name, 'w')
  for key in data:
    if(len(key)>0):
      content = "<h4 class=\"text-center\">%s</h4><div class=\"row\">" %(key)
      for item in data[key]:
          url_present = True if len(item[2])>0 else False
          img = item[1] if len(item[1])>0 else "images/profpic_man.jpg"
          img_tag = "<img class=\"img-circle student_image\" src=\"%s\">"%(img)
          assert len(item[0])>0
          name = "<a href='%s'>%s</a>"%(item[2], item[0]) if(url_present) else item[0]
          name_tag = "<span>%s</span>"%(name)
          entry = img_tag + name_tag
          content += "<div class='col-md-3 col-xs-6 m-b-10'>%s</div>" %(entry)
      content+= "</div>"
      target.write(content)
  print("Generated File in %s"%(file_name))
  target.close()

def Month(val):
  assert val > 0
  assert val <=12
  dictionary = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
  return dictionary[val]

def content_month_year(month,year):
  template = " <div class=\"row\"><div class=\"col-md-1 newsNext\"><h2>%s</h2></div><div class=\"col-md-1\"><h2>%s</h2></div><div class=\"col-md-10\">&nbsp;</div></div>"%(year, Month(month))
  return template

def template_news(text,url):
  news_item = "<a target=\"_blank\" href=\"%s\">%s</a>"%(url,text) if len(url) > 0 else text
  return "<div class=\"row\"><div class=\"col-md-1\">&nbsp;</div><div class=\"col-md-1\">&nbsp;</div><div class=\"col-md-10 newsItem newsNext\">%s</div></div>"%news_item

def generate_news_page(file_name):
  source_file = 'News.txt'
  studentReader = csv.reader(open(source_file, 'rb'), delimiter=',', skipinitialspace=True)
  data = OrderedDict()
  for row in studentReader:
    assert len(row)>=3 
    month_year = (int(row[0]), row[1])
    if(month_year in data):
      data[month_year].append(row[2:])
    else:
      data.update({month_year: [row[2:]]})
  # print data
  data_year_based = defaultdict(dict)
  for key in data:
    yr_dict = data_year_based[key[1]]
    yr_dict.update({key[0]: (data[key])})
  data_year_based = OrderedDict(sorted(data_year_based.items()))

  target = open(file_name, 'w')

  content = "<h4 class=\"text-center\">%s</h4>"%("News and Events")
  for year in data_year_based:
    month_dict = data_year_based[year]
    month_dict = OrderedDict(sorted(month_dict.items()))
    for month in (month_dict):
      content += content_month_year(month,year)
      for item in month_dict[month]:
        content+= template_news(item[0],item[1]) 
  target.write(content)
  target.close()
  print("Generated File in %s"%(file_name))
  # for key in data:
  #   if(len(key)>0):
  #     content = "<h4 class=\"text-center\">%s</h4><div class=\"row\">" %(key)
  #     for item in data[key]:
  #         url_present = True if len(item[2])>0 else False
  #         img = item[1] if len(item[1])>0 else "images/profpic_man.jpg"
  #         img_tag = "<img class=\"img-circle student_image\" src=\"%s\">"%(img)
  #         assert len(item[0])>0
  #         name = "<a href='%s'>%s</a>"%(item[2], item[0]) if(url_present) else item[0]
  #         name_tag = "<span>%s</span>"%(name)
  #         entry = img_tag + name_tag
  #         content += "<div class='col-md-3 col-xs-6 m-b-10'>%s</div>" %(entry)
  #     content+= "</div>"
  #     target.write(content)
  # print("Generated File in %s"%(file_name))
  # target.close()


def main():
  if(sys.argv[1] == "students"):
    generate_students_page("students_content.txt")
  elif(sys.argv[1] == "news"):
    generate_news_page("news_content_tmp.txt")
  else:
    print "UNKNOWN OPTION USED"

if __name__ == "__main__":
  main()