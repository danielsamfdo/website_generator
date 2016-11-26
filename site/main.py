import os
import re
import bibtexparser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Publications:
    """A simple example class"""
    def __init__(self, pub_type):
        self.pub_type = pub_type
    
    def print_publication(self):
        if(hasattr(self,'month')):
            month = self.month
        else:
            month = ""
        if('note' in self.entry):
            note = "<br/>" + self.entry['note']
        else:
            note = ""
        if('pages' in self.entry):
            pages = self.entry['pages']
        else:
            pages = ""
        title = self.title
        if('link' in self.entry):
          title = "<a href='%s'>%s</a>" %(self.entry['link'], self.title)
          # print  "<a href='%s'>%s</a>" %(self.entry['url'], self.title)        
        if(self.pub_type == "conference"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s' %(title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "techreport"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %(title, self.author, self.entry["institution"], self.entry["number"], month, self.year)
        elif(self.pub_type == "phdthesis"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, "PhD Thesis",self.entry["institution"], month, self.year)
        elif(self.pub_type == "ugthesis"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, "Undergraduate Thesis",self.entry["institution"], month, self.year)
        elif(self.pub_type == "journal"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s %s, %s' %( title, self.author, self.entry["journal"], self.entry["volume"], pages, month, self.year, note)
        elif(self.pub_type == "workshop"):
            s ='%s<br/> %s,<br/> %s, %s %s' %( title, self.author, self.entry["booktitle"], month, self.year)
        elif(self.pub_type == "bookchapter"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s' %( title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "book"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s' %( title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "misc"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, self.entry["booktitle"], self.entry["institution"], month, self.year)
        return s

def get_bib_entries(file_name):  
  with open(file_name) as bibtex_file:
    bibtex_str = bibtex_file.read()

  bib_database = bibtexparser.loads(bibtex_str)

  return (bib_database)

def add_category_to_dblp_file(file_name, new_file_name):
  f = open(file_name, 'r')
  main_file = open(new_file_name,'w')
  for i in f.readlines(): 
      if(re.search("bibsource",i)):
          txt = re.sub("\n",",\n",i)
          main_file.write(txt)
      else:
          if(i=="}\n"):
              main_file.write('  catteggory = "SELECT Network",\n')# TO ADD A CATTEGGORY TO THE FILE
          main_file.write(i)
  f.close()
  main_file.close()
  f.close()

def entry_type(Ent_type):
    hash_values = {"inproceedings": "conference", "techreport": "techreport", "phdthesis":"phdthesis", "mastersthesis": "ugthesis", "article": "journal", "proceedings":  "workshop", "inbook" : "bookchapter", "misc" : "misc", "book":"book"}
    return hash_values[Ent_type]

def check_if_unique(list_of_pubs, check_pub):
    for pub in list_of_pubs:
        if(pub.title.lower() == check_pub.title.lower()):
            if(pub.year==check_pub.year):
                return False
    return True

def month_hash():
    return {"Jan":"January", "Feb": "February", "Mar": "March", "Apr":"April", "May":"May", "Jun":"June", "Jul":"July", "Aug":"August","Sep":"September","Oct":"October", "Nov":"November", "Dec":"December"}

def month(text):
    val = month_hash()
    return val[text]

def process_text(text):
    text = re.sub("[{}]","",text)
    text = re.sub("\n"," ",text)
    text = ' '.join(x.strip() for x in text.split())
    return text

add_category_to_dblp_file('dblp.bib','main_dblp.bib')
my_pubs_bib_database = get_bib_entries('mypubs.bib')
dblp_bib_database = get_bib_entries('main_dblp.bib')

entries = []
non_entries = []
conferences = []
techreports = []
phdthesis = []
ugthesis = []
journals = []
workshops = []
bookchapters = []
books = []
misc = []


min_year = 1999
max_year = 1999
for i in my_pubs_bib_database.entries + dblp_bib_database.entries:
    if(not(u'author' in i.keys())):
        non_entries.append(i)
    else:
        if(re.search("arun",i[u'author'], re.IGNORECASE)):
            #print entry_type(i['ENTRYTYPE'])
            x = Publications(entry_type(i['ENTRYTYPE']))
            x.title = process_text(i['title'])
            
            i['title'] = process_text(i['title'])
            x.author = process_text(i['author'])
            i['author'] = process_text(i['author'])
            x.entry = i
            if(not 'year' in i):
                print "YEAR IS MISSING FOR "
                print i
            x.year = int(i['year'])
            if('month' in i):
                x.month = i['month']
            elif('timestamp' in i):
                x.month = month(i['timestamp'].split()[2])
            #else:
            #    print i
            if(x.year > max_year):
                max_year = x.year
            if(x.pub_type == "conference"):
                if(check_if_unique(conferences, x)):
                    conferences.append(x)
                    entries.append(x)
            if(x.pub_type == "techreport"):
                if(check_if_unique(techreports, x)):
                    techreports.append(x)
                    entries.append(x)
            if(x.pub_type == "phdthesis"):
                if(check_if_unique(phdthesis, x)):
                    phdthesis.append(x)
                    entries.append(x)
            if(x.pub_type == "ugthesis"):
                if(check_if_unique(ugthesis, x)):
                    ugthesis.append(x)
                    entries.append(x)
            if(x.pub_type == "journal"):
                if(check_if_unique(journals, x)):
                    journals.append(x)
                    entries.append(x)
            if(x.pub_type == "workshop"):
                if(check_if_unique(workshops, x)):
                    workshops.append(x)
                    entries.append(x)
            if(x.pub_type == "bookchapter"):
                if(check_if_unique(bookchapters, x)):
                    bookchapters.append(x)
                    entries.append(x)
            if(x.pub_type == "misc"):
                if(check_if_unique(misc, x)):
                    misc.append(x)
                    entries.append(x)
            if(x.pub_type == "book"):
                if(check_if_unique(books, x)):
                    books.append(x)
                    entries.append(x)
years_entries =[]
for i in reversed(range(min_year,max_year+1)) :
    pubs = []
    year_entry = []
    for entry in entries:
        if(entry.year == i):
            pubs.append(entry)
    no_month_entries = []
    for month in reversed(month_hash().values()):
            for pub in pubs:
                if(hasattr(pub, 'month')):
                    if(month==pub.month):
                        year_entry.append(pub) #pub.title, pub.month, pub.year
                else:
                    if(check_if_unique(no_month_entries, pub)):
                        no_month_entries.append(pub)

    for nm_entry in no_month_entries:
        year_entry.append(nm_entry)
        #print pub.title, pub.year

    years_entries.append(year_entry)

target = open("all.html", 'w')
yr = max_year
for year_entry in years_entries:
    s = "<h5>%s</h5>" %(yr)
    yr-=1
    target.write(s)
    for entry in year_entry:
        s = "<li>%s</li>" %((entry.print_publication()))
        target.write(s)
target.close()
print "Test"
target = open("select_new.html", 'w')
yr = max_year
for year_entry in years_entries:
    
    s = ""
    for entry in year_entry:
        if(re.search("SELECT",entry.entry["catteggory"])):
            s+= "<li>%s</li><br/>" %((entry.print_publication()))
            
    if(len(year_entry)>0):
        header = "<h5>%s</h5>" %(yr)    
        target.write(header+"<ul>"+s+"</ul>")
    yr-=1
target.close()
