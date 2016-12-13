import os
import re
import bibtexparser
import scholarly
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import pickle
import sys
import htmlentitydefs as entity
reload(sys)
sys.setdefaultencoding('utf-8')

def convert_foreign_characters(text):
    text = re.sub(r"\\'(.)", r"&\1acute;", text)
    text = re.sub(r"\\&apos;(.)", r"&\1acute;", text)
    text = text.replace("\\&amp;","&")
    text = text.replace("amp;","") # there were a few inconsistent cases and so i have added this case alone
    # print text, "------------"
    text = text.replace("\\&", "&")
    # text = decode_to_entity(text)

    # SOME UNWANTED CHAR THAT CAME IN BECAUSE OF UTF-8
    text = text.replace("&pound;", "")
    text = text.replace("&copy;", "")
    text = text.replace("Menasch&Atilde;","Menasch&eacute;")
    text = text.replace("Arag&Atilde;&pound;o","Arag&atilde;o")
    text = text.replace("Le&Atilde;o","Le&atilde;o")
    return re.sub(r"\\\~(.)", r"&\1tilde;", text)
    

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def decode_to_entity(s):
    # Does not work quite well for all instances "
    t = ""
    for i in s:
            if ord(i) in entity.codepoint2name:
                    name = entity.codepoint2name.get(ord(i))
                    t += "&" + name + ";"
            else:
                    t += i
    return t

def foreign_accents(author):
    # print author

    author = re.sub(r"\\&apos;(.)", r"&\1acute;", author)
    # print author,"-------------"
    return re.sub(r"\\\~(.)", r"&\1tilde;", author)

def remove_unwanted_characters(text):
    # print text
    text = text.replace("\\&amp;","&")
    text = text.replace("amp;","") # there were a few inconsistent cases and so i have added this case alone
    # print text, "------------"
    text = text.replace("\\&", "&")
    return text

def remove_set_brackets(text):
    return re.sub("[{}]","", text)


class Publications:
    """A simple example class"""
    def __init__(self, pub_type, gs=False):
        self.pub_type = pub_type
        self.google_scholar = gs

    def print_bibtex(self):
      if(hasattr(self, "bibtex_string")):
        bibtex_str = re.sub("\n","<br>",self.bibtex_string)
        # bibtex_str = re.sub(".*catteggory.*={.*},?","<br>",self.bibtex_string)
        return "<div class='bib_tex_show_hide'>[+]Show Bib</div><div class='bibentry'><div class='bibtexentry'>%s</div></div>"  %(bibtex_str)
      else:
        return ""

    def gscholar_print_extra_if_present(self):
      extra = ""
      volume = ""
      if 'volume' in self.entry:
        volume = "Volume: %s, " %self.entry['volume']
      pages = ""
      if 'pages' in self.entry:
        pages = "Pages: %s, " %self.entry['pages']
      number = ""
      if 'number' in self.entry:
        pages = "Number: %s, " %self.entry['number']
      journal = ""
      if 'journal' in self.entry:
        journal = "Journal : %s, " %self.entry['journal']
        extra+= journal + volume + number + pages 
      if(len(extra)>0):
        return "<br>"+extra
      return ""

    def print_abstract(self):
      if(hasattr(self, "abstract")):
        # print self.entry
        x = str(self.abstract)
        abst = striphtml(x)
        # abst = re.sub(r'(<br>)|(<br/>)',"",x)
        return "<br/><div class='abstract_show_hide'>[+]Show Abstract</div><div class='ab_entry'><div class='abstractentry'>%s</div></div>"  %(abst)
      else:
        return ""

    def google_scholar_print(self):
      title = self.title
      if('url' in self.entry):
        title = "<a href='%s'>%s</a>" %(self.entry['url'], self.title)
      author = ""
      if(self.author!= None and len(self.author)>0):
        author = "<br>" + self.author
      # if('author' in self.entry):
      #   author = "<br>" + self.entry['author']
      abstract = ""
      if(hasattr(self,"abstract")):
        abstract = self.print_abstract()
      s = "%s %s %s %s" %(title,author,abstract, self.gscholar_print_extra_if_present())
      return s

    def abstract_bibtex(self):
      return self.print_abstract() + self.print_bibtex()

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
            pages = "pages:" + self.entry['pages']
        else:
            pages = ""
        if('journal' in self.entry):
            self.entry['journal'] = remove_set_brackets(self.entry['journal'])
        if("booktitle" in self.entry):
            self.entry['booktitle'] = remove_set_brackets(self.entry['booktitle'])
        if("volume" in self.entry):
            volume = "Volume:" + self.entry["volume"]


        title = remove_unwanted_characters(self.title)


        if('link' in self.entry):
          title = "<a href='%s'>%s</a>" %(self.entry['link'], title)
          # print  "<a href='%s'>%s</a>" %(self.entry['url'], self.title)        

        # author = self.author
        self.author = foreign_accents(self.author)

        if(self.google_scholar == True):
            s = self.google_scholar_print()
        elif(self.pub_type == "conference"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s' %(title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "techreport"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %(title, self.author, self.entry["institution"], self.entry["number"], month, self.year)
        elif(self.pub_type == "phdthesis"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, "PhD Thesis",self.entry["institution"], month, self.year)
        elif(self.pub_type == "ugthesis"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, "Undergraduate Thesis",self.entry["institution"], month, self.year)
        elif(self.pub_type == "journal"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s %s, %s' %( title, self.author, self.entry["journal"], volume, pages, month, self.year, note)
        elif(self.pub_type == "workshop"):
            s ='%s<br/> %s,<br/> %s, %s %s' %( title, self.author, self.entry["booktitle"], month, self.year)
        elif(self.pub_type == "bookchapter"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s' %( title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "book"):
            s ='%s<br/> %s,<br/> %s, %s %s, %s' %( title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "misc"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, self.entry["booktitle"], self.entry["institution"], month, self.year)
        s = s.rstrip()# remove empty space if things are empty then remove a comma at the end if present .
        if(s[-1]==','):
            s = s[:-1] 
        s = s + " " + self.abstract_bibtex()
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

def check_word_containment(title1, title2):
  title1 = re.sub("[.)(]","",title1)
  title2 = re.sub("[.)(]","",title2)
  title2 = re.sub("[-]"," ",title2)
  title1 = re.sub("[-]"," ",title1)
  tokens1 = title1.lower().split()
  tokens2 = title2.lower().split()

  if "best" in tokens2:
    tokens2.remove("best") 

  if "awarded" in tokens2:
    tokens2.remove("awarded") 
  if "student" in tokens2:
    tokens2.remove("student")
  if "paper" in tokens2:
    tokens2.remove("paper")
  tcnt=0
  cnt=0
  for token in tokens2:
    if token in tokens1:
      cnt+=1
    tcnt+=1
  if(tcnt-cnt<=1):
    print title1, title2
    if(abs(len(tokens2)-len(tokens1))<=3):
      return True
    else:
      return False
  else:
    return False

def check_if_unique(list_of_pubs, check_pub):
    for pub in list_of_pubs:
        if(pub.title.lower() == check_pub.title.lower()):
          if(pub.year==check_pub.year):
            return False
        elif(check_word_containment(pub.title, check_pub.title)):
          if(pub.year==check_pub.year):
            return False

    return True

def returnSimilarPub(list_of_pubs, check_pub_title, check_pub_year, check_year):
    for pub in list_of_pubs:
        if(pub.title.lower() == check_pub_title.lower()):
          if(check_pub_year!=None):
            if(pub.year==check_pub_year):
              return pub
          else:
            return pub
    for pub in list_of_pubs:
        if(check_word_containment(pub.title, check_pub_title)):
          if(check_pub_year!=None):
            if(pub.year==check_pub_year):
              return pub
          else:
            return pub

    return None

def list_months_rev():
  return ["December", "November", "October", "September", "August", "July", "June", "May", "April", "March", "February", "January"]

def month_hash():
    return {"Jan":"January", "Feb": "February", "Mar": "March", "Apr":"April", "May":"May", "Jun":"June", "Jul":"July", "Aug":"August","Sep":"September","Oct":"October", "Nov":"November", "Dec":"December"}

def month(text):
    val = month_hash()
    return val[text]

def add_google_scholar_entries(existing_publications):
  f = open('gs_entries_prof_arun.dat', 'r')
  entries = pickle.load(f)
  bib_entries = []
  ignore = []
  ignore = ["Timothy Wood","Publication list","Abstract/Details","Aruna Balasubramanian"]
  for ent in entries:
    # if(re.match("venkataramani",ent['author'],re.IGNORECASE)):
      if(ent['title'] not in ignore):
        bib_entries.append(ent)
        print "####******%s******" %ent['title']
      else:
        print "******%s******" %ent['title']
    # else:
      # print "IGNORED ---------> " + ent['title']
  f.close()
  non_entries = []
  for pub_bib in bib_entries:
    if('year' in pub_bib):
      yr = int(pub_bib['year'])
      check_year = True
    else:
      yr = None
      # print pub_bib['title'] + "has no year associated with it "
      check_year = False    
    similar_pub = returnSimilarPub(existing_publications, pub_bib['title'], yr, check_year)
    if(similar_pub):
      if('abstract' in pub_bib):
        # pub_entry_dict =similar_pub.entry
        similar_pub.abstract = pub_bib['abstract']

        # print "Abstract Added for %s" %(pub_bib['title'])  
        # similar_pub.entry = pub_entry_dict
      # else:
        # print "No abstract present"
    else:
      # print "No similar PUB present for %s" %(pub_bib['title'])
      # print "Adding Publication %s" %(pub_bib['title'])

      new_pub = Publications("google_scholar",True)
      new_pub.bib = pub_bib
      # print pub_bib
      new_pub.title = pub_bib['title']
      new_pub.author = ""
      if('author' in pub_bib):#PATENTS DID NOT HAVE AUTHOR NAMES
        new_pub.author = pub_bib['author']

      if('year' in pub_bib):
        new_pub.year = pub_bib['year']
      else:
        new_pub.year = None
      new_pub.entry = pub_bib
      non_entries.append(new_pub)
      existing_publications.append(new_pub)
  print len(non_entries)
  for i in non_entries:
    print i.title
  return non_entries

def import_publications_from_google_scholar(existing_publications):
  author = next(scholarly.search_author('Arun Venkataramani')).fill()
  entries = []
  for pub in author.publications:
    pub.fill()
  for pub in author.publications:
    similar_pub = returnSimilarPub(existing_publications, pub.bib['title'], int(pub.bib['year']))
    if(similar_pub):
      if('abstract' in pub.bib):
        print "Abstract Added for %s" %(pub.title)  
        similar_pub.entry['abstract'] = pub.bib['abstract']
      else:
        print "No abstract present"
    else:
      print "NO similar PUB present for %s" %(pub.title)
  return 

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
                if(check_if_unique(conferences+journals, x)):
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
                if(check_if_unique(journals+conferences, x)):
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

for entry in entries:
  db = BibDatabase()
  db.entries = [entry.entry]
  writer = BibTexWriter()
  entry.bibtex_string = writer.write(db)

print "$$$$$$$$$$$$$$$$$$$$$$$$$$"

new_gs_entries = add_google_scholar_entries(entries)

non_year_entries = []
for gs_entry in new_gs_entries:
  if(gs_entry.year == None):
    non_year_entries.append(gs_entry)

years_entries =[]
for m in (list_months_rev()):
  print m
for i in reversed(range(min_year,max_year+1)) :
    pubs = []
    year_entry = []

    for entry in entries:
        if(entry.year == i):
          pubs.append(entry)
    no_month_entries = []
    for month in list_months_rev():
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
      if(entry.google_scholar == True or re.search("SELECT",entry.entry["catteggory"])):
          s+= "<li>%s</li><br/>" %((entry.print_publication()))
    if(len(year_entry)>0):
        header = "<h5>%s</h5>" %(yr)    
        s = convert_foreign_characters(s)
        s = s.encode("utf-8")

        target.write(header+"<ul>"+s+"</ul>")
    yr-=1
s=""
for entry in non_year_entries:
  if(entry.google_scholar == True or re.search("SELECT",entry.entry["catteggory"])):
          s+= "<li>%s</li><br/>" %((entry.print_publication()))
if(len(non_year_entries)>0):
    header = "<h5>%s</h5>" %("Others")    
    s = convert_foreign_characters(s)
    s = s.encode("utf-8")

    target.write(header+"<ul>"+s+"</ul>")
target.close()
