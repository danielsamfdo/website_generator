import os
import re
import bibtexparser
import scholarly
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import pickle
import cPickle as pl
import sys
import htmlentitydefs as entity
import copy
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def convert_foreign_characters(text):
    text = text.replace("\\&amp;","&")
    text = text.replace("amp;","") # there were a few inconsistent cases and so i have added this case alone
    text = text.replace("\\&", "&")
    return re.sub(r"\\\~(.)", r"&\1tilde;", text)

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def foreign_accents(author):
    author = re.sub(r"\\&apos;(.)", r"&\1acute;", author)
    return re.sub(r"\\\~(.)", r"&\1tilde;", author)

def remove_unwanted_characters(text):
    text = text.replace("\\&amp;","&")
    text = text.replace("amp;","") # there were a few inconsistent cases and so i have added this case alone
    text = text.replace("\\&", "&")
    return text

def remove_set_brackets(text):
    return re.sub("[{}]","", text)

class Publications:
    def __init__(self, pub_type, gs=False, isPatent=False):
        self.pub_type = pub_type
        self.google_scholar = gs
        self.patent = isPatent

    def print_bibtex(self):
      if(hasattr(self, "bibtex_string")):
        bibtex_str = copy.copy(self.bibtex_string)
        # REMOVE CATEGORY IN THE DISPLAY
        bibtex_str = re.sub("catteggory.*[=].*[{].*[}],\n", "", bibtex_str)
        # REMOVE NOTE IN THE DISPLAY
        bibtex_str = re.sub("note.*[=].*[{].*[}],\n", "", bibtex_str)
        bibtex_str = re.sub("@mastersthesis","@ugthesis", bibtex_str) # @UGTHESIS is not an actually bibtype but it is present in mypubs
        bibtex_str = re.sub("\n", "<br>", bibtex_str)
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
        x = str(self.abstract)
        abst = striphtml(x)
        return "<br/><div class='abstract_show_hide'>[+]Show Abstract</div><div class='ab_entry'><div class='abstractentry'>%s</div></div>"  %(abst)
      else:
        return ""

    def google_scholar_print(self):
      title = self.title
      if('url' in self.entry):
        title = "<a href='%s'>%s</a>" %(self.entry['url'], self.title)
      assert len(self.title)>0
      assert len(self.author)>0
      author = "<br>" + self.author
      abstract = ""
      if(hasattr(self,"abstract")):
        abstract = self.print_abstract()
      s = "%s %s %s %s" %(title,author, self.gscholar_print_extra_if_present(),abstract)
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
            pages = "Pages: %s, " %self.entry['pages']
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

        self.author = foreign_accents(self.author)
        if(self.google_scholar == True):
            s = self.google_scholar_print()
        elif(self.pub_type == "conference"):
            s = conference_template(title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "techreport"):
            s = techreport(title, self.author, self.entry["institution"], self.entry["number"], month, self.year)
            # '%s<br/> %s,<br/> %s, %s, %s %s' %(title, self.author, self.entry["institution"], self.entry["number"], month, self.year)
        elif(self.pub_type == "phdthesis"):
            s = thesis_template( title, self.author, "PhD Thesis",self.entry["institution"], month, self.year)
        elif(self.pub_type == "ugthesis"):
            s = thesis_template( title, self.author, "Undergraduate Thesis",self.entry["institution"], month, self.year)
        elif(self.pub_type == "journal"):
            s = journal_template(title, self.author, self.entry["journal"], volume, pages, month, self.year, note)
            # s ='%s<br/> %s,<br/> %s, %s %s, %s %s, %s' %( title, self.author, self.entry["journal"], volume, pages, month, self.year, note)
        elif(self.pub_type == "workshop"):
            s =workshop_bookchapter_book_template( title, self.author, self.entry["booktitle"], month, self.year)
        elif(self.pub_type == "bookchapter"):
            s =workshop_bookchapter_book_template( title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "book"):
            s =workshop_bookchapter_book_template( title, self.author, self.entry["booktitle"], month, self.year, note)
        elif(self.pub_type == "misc"):
            s ='%s<br/> %s,<br/> %s, %s, %s %s' %( title, self.author, self.entry["booktitle"], self.entry["institution"], month, self.year)
        s = s.rstrip()# remove empty space if things are empty then remove a comma at the end if present .
        if(s[-1]==','):
            s = s[:-1] 
        if(self.google_scholar == False):
            s = s + " " + self.abstract_bibtex()
        return s

def workshop_bookchapter_book_template( title, author, booktitle, month, year, note=""):
  assert len(author) > 10
  content="%s<br/> %s, <br/>"%(title, author)
  content+="%s, %s %s,"%(booktitle,month,year)
  content+=note
  return content

def journal_template(title, author, journal, volume, pages, month, year, note):
  assert len(author) > 10
  content="%s<br/> %s, <br/>"%(title, author)
  content+="%s, %s %s"%(journal,volume,pages)
  if(not re.search(" "+str(year),journal)):
    content+=" %s %s,"%(month,year)
  content+=note
  # if(year==2016):
  #   print pages
  #   print "#########"+month,str(year),content
  return content

def thesis_template(title, author, thesis_title, institution, month, year):
  assert len(author) > 10
  content="%s<br/> %s, <br/>"%(title, author)
  content+="%s, %s,"%(thesis_title, institution)
  content+=" %s %s,"%(month,year)
  return content

def conference_template(title, author, booktitle, month, year, note):
  assert len(author) > 10
  content="%s<br/> %s, <br/>"%(title, author)
  content+="%s,"%(booktitle)
  if(not re.search(" "+str(year),booktitle)):
    # print "Came in"
    content+=" %s %s,"%(month,year)
  # else:
  #   print "*******%s "%(title)
  content+=note
  return content

def techreport(title, author, institution, number, month, year):
  assert len(author) > 10
  content="%s<br/> %s, <br/>"%(title, author)
  content+="%s, %s"%(institution, number)
  content+=" %s %s,"%(month,year)
  return content

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
  title1 = re.sub("[.)(:,]","",title1)
  title2 = re.sub("[.)(:,]","",title2)
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
  for token in (tokens2):
    if token in tokens1:
      cnt+=1
    tcnt+=1
  if(tcnt-cnt<=1):
    if(abs(len(tokens2)-len(tokens1))<=3):
      return True
    else:
      return False
  else:
    return False

def check_if_unique(list_of_pubs, check_pub):
    IGNORE_PUBS = ["Augmenting Mobile 3G Using WiFi: Measurement, Design, and Implementation"]
    REQUIRED_PUB_IDS = ['bundling','bundling2']
    if(hasattr(check_pub,'ID') and check_pub.entry['ID'] in REQUIRED_PUB_IDS):
      return True
    if(check_pub.title in IGNORE_PUBS):
      return False
    for pub in list_of_pubs:
        if(pub.title.lower() == check_pub.title.lower()):
          if(pub.year==check_pub.year):
            return False
            # if(pub.google_scholar):
            #   return False
            # # print pub.title
            # elif(not hasattr(pub,'month')):
            #   return False
            # elif(hasattr(pub,'month') and hasattr(check_pub,'month') and pub.month==check_pub.month):
            #   print pub.title
            #   return False
            # else:
            #   return False
        elif(check_word_containment(pub.title, check_pub.title)):
          if(pub.year==check_pub.year):
            return False

    return True

def pub_similar_year(pub, check_year,check_pub_year):
  if(check_year):
    if(pub.year == check_pub_year):
      return pub
  else:
    return pub
  return None

# THIS FUNCITON IS USED FOR CHECKING FOR GOOGLE SCHOLAR ENTRIES, IF THERE ALREADY EXISTS AN ENTRY IN THE OTHER PUBLICATIONS.
def returnSimilarPub(list_of_pubs, check_pub_title, check_pub_year, check_year):
    IGNORE_PUBS = {"mechanisms and algorithms for aggressive replication systems": "Mechanisms and Algorithms for Large-Scale Replication Systems", "towards a quantitative comparison of location-independent network architectures" : "Towards a quantitative comparison of location-independent network architectures"}
    if(check_pub_title.lower() in IGNORE_PUBS.keys()):
        for pub in list_of_pubs:
          if(pub.title == IGNORE_PUBS[check_pub_title.lower()]):
            return pub
    for pub in list_of_pubs:
        if(pub.title.lower() == check_pub_title.lower()):
          pub = pub_similar_year(pub, check_year,check_pub_year)
          if(pub!=None):
            return pub
    for pub in list_of_pubs:
        if(check_word_containment(pub.title, check_pub_title)):
          pub = pub_similar_year(pub, check_year,check_pub_year)
          if(pub!=None):
            return pub
    return None

def list_months_rev():
  return ["December", "November", "October", "September", "August", "July", "June", "May", "April", "March", "February", "January"]

def month_hash():
    return {"Jan":"January", "Feb": "February", "Mar": "March", "Apr":"April", "May":"May", "Jun":"June", "Jul":"July", "Aug":"August","Sep":"September","Oct":"October", "Nov":"November", "Dec":"December"}

def month(text):
    val = month_hash()
    return val[text]

def json_information(file_name):
  with open(file_name) as data_file:
    data = json.load(data_file)
  return (data)

def populate_abstract(pubs):
  pubs_abstracts = json_information('abstract_publications.json')
  for item in pubs_abstracts:
    for pub_item in pubs:
      if('ID' in item and 'ID' in pub_item.entry and item['ID'] == pub_item.entry['ID']):
        pub_item.abstract = item['abstract']
      elif(not 'ID' in item and item['title'] == pub_item.title and pub_item.google_scholar):
        pub_item.abstract = item['abstract']

def populate_information_for_patent(pub, patents):

  for item in patents:
    if(item['title'] == pub.title):
      pub.author = item['author']
      pub.abstract = item['abstract']

def add_google_scholar_entries(existing_publications):
  f = open('gs_entries_prof_arun.dat', 'r')
  entries = pickle.load(f)
  patents = json_information('patents.json')
  bib_entries = []
  ignore = []
  ignore = ["Timothy Wood","Publication list","Abstract/Details","Aruna Balasubramanian", "Energy in Communication, Information, and Cyber-physical Systems (E6) Technical Program Committee", "connect with us", "Proceedings of the Sixth International Workshop on Web Caching and Content Distribution"]
  for ent in entries:
      # print ent['title']
    # if(re.match("venkataramani",ent['author'],re.IGNORECASE)):
      if(ent['title'] not in ignore):
        bib_entries.append(ent)
        # print "####******%s******" %ent['title']
      # else:
        # print "******%s******" %ent['title']
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
        similar_pub.abstract = pub_bib['abstract']
        # pub_entry_dict =similar_pub.entry
        # if(hasattr() and len(similar_pub.abstract)==0):
          

        # print "Abstract Added for %s" %(pub_bib['title'])  
        # similar_pub.entry = pub_entry_dict
      # else:
        # print "No abstract present"
    else:
      # print "No similar PUB present for %s" %(pub_bib['title'])
      # print "Adding Publication %s" %(pub_bib['title'])
      patent = True if ('url' in pub_bib and re.search("patent",pub_bib['url'])) else False
      # if(patent):
        # print pub_bib['title']+"is a Patent"
      new_pub = Publications("google_scholar",True, isPatent=patent)
      new_pub.bib = pub_bib
      # print pub_bib
      new_pub.title = pub_bib['title']
      new_pub.author = ""
      if('author' in pub_bib):#PATENTS DID NOT HAVE AUTHOR NAMES
        new_pub.author = pub_bib['author']
      if patent:
        populate_information_for_patent(new_pub, patents)
      if('abstract' in pub_bib):
        new_pub.abstract = pub_bib['abstract']
      if('year' in pub_bib):
        new_pub.year = pub_bib['year']
      else:
        new_pub.year = None
      new_pub.entry = pub_bib
      new_pub.conference_name = conference_type(pub_bib)
      non_entries.append(new_pub)
      existing_publications.append(new_pub)
  # print len(non_entries)
  # for i in non_entries:
  #   print i.title
  return non_entries

def save_publications_from_google_scholar():
  author = next(scholarly.search_author('Arun Venkataramani')).fill()
  entries = []
  for pub in author.publications:
      pub.fill()
      print "Fetching %s"%(pub.bib['title'])
  for pub in author.publications:
      entries.append(pub.bib)
  pl.dump(entries, open( "gs_entries_prof_arun.dat", "wb" ) )
  

# def import_publications_from_google_scholar(existing_publications):
#   author = next(scholarly.search_author('Arun Venkataramani')).fill()
#   entries = []
#   for pub in author.publications:
#     pub.fill()
#   for pub in author.publications:
#     similar_pub = returnSimilarPub(existing_publications, pub.bib['title'], int(pub.bib['year']))
#     if(similar_pub):
#       if('abstract' in pub.bib):
#         print "Abstract Added for %s" %(pub.title)  
#         similar_pub.entry['abstract'] = pub.bib['abstract']
#       else:
#         print "No abstract present"
#     else:
#       print "NO similar PUB present for %s" %(pub.title)
#   return 

def conference_type(bib_entry):
  if('journal' in bib_entry):
    if(re.search('ieee',bib_entry['journal'],re.IGNORECASE)):
      return "ieee"
    elif(re.search('acm',bib_entry['journal'],re.IGNORECASE)):
      return "acm"
  elif('booktitle' in bib_entry):
    if(re.search('ieee',bib_entry['booktitle'],re.IGNORECASE)):
      return "ieee"
    elif(re.search('acm',bib_entry['booktitle'],re.IGNORECASE)):
      return "acm"
  else:
    return ""


def process_text(text):
    text = re.sub("[{}]","",text)
    text = re.sub("\n"," ",text)
    text = ' '.join(x.strip() for x in text.split())
    return text


def conference_publications(pub_entries):
  target =  open("conference_publications.txt", 'w')
  acceptable_conferences = ['ieee', 'acm']
  for acceptable_conference in acceptable_conferences:
    content = ""
    for pub in pub_entries:
      # print pub.conference_name
      if(pub.conference_name == acceptable_conference):
        content+="<li>%s</li><br/>" %((pub.print_publication()))
    if(len(content)>0):
      header =  "<h5>%s</h5>" %(acceptable_conference.upper())
      content = convert_foreign_characters(content)
      target.write(header+"<ul>"+content+"</ul>")
  target.close()

def gather_categories(pub_entries):
  categories = set()
  for pub in pub_entries:
    if('catteggory' in pub.entry):
      if(re.search('SELECT',pub.entry['catteggory'],re.IGNORECASE)):
        category = re.sub('SELECT','', pub.entry['catteggory'],re.IGNORECASE)
        tokens = set(category.lower().split())
        categories = categories.union(tokens)
  return categories

def categories_publications(pub_entries):
  target =  open("categories_publications.txt", 'w')
  categories = gather_categories(pub_entries)
  # print categories
  for category in categories:
    content = ""
    for pub in pub_entries:
      if('catteggory' in pub.entry and re.search('SELECT',pub.entry['catteggory'],re.IGNORECASE) and re.search(category,pub.entry['catteggory'],re.IGNORECASE)):
        content+="<li>%s</li><br/>" %((pub.print_publication()))
    if(len(content)>0):
      header =  "<h5>%s</h5>" %(category.upper())
      content = convert_foreign_characters(content)
      target.write(header+"<ul>"+content+"</ul>")
  target.close()


def generate_publications_content(target_file):
  target = open(target_file,"w")
  nav_tabs = ""
  nav_tab_content = ""
  config = {'Year':"year_publications.html",'Conference':"conference_publications.txt"}
  active_tab = "active"
  for key in config:
    nav_tabs += "<li><a data-toggle='tab' href='#%s'>%s</a></li>" %(key,key)
    file = open(config[key],'r')
    file_content = file.read()
    nav_tab_content += "<div id='%s' class='tab-pane %s'>%s</div>" %(key,active_tab,file_content)
    active_tab=""
  nav_header = "<ul class='nav nav-tabs'>%s</ul>" %(nav_tabs)
  nav_tabs_content = "<div class='tab-content'>%s</div>" %nav_tab_content
  target.write(nav_header+nav_tabs_content)
  target.close()

def assert_years_entries(yr, year_entry):
  check_entries = { 2016: ['Identifying and Addressing Reachability and Policy Attacks in \"Secure\" BGP', 'msocket: System support for mobile, multipath, and middlebox- agnostic applications'],
                    2015: ['Measurement and modeling of user transitioning among networks'],
                    2014: ['MobilityFirst: a mobility-centric and trustworthy internet architecture','Pros \\&amp; cons of model-based bandwidth control for client- assisted content delivery','VMShadow: optimizing the performance of latency-sensitive virtual desktops in distributed clouds','A global name service for a highly mobile internetwork','Towards a quantitative comparison of location-independent network architectures','CDN Pricing and Investment Strategies under Competition'],
                    2013: ['Content Availability and Bundling in Swarming Systems','VMShadow: optimizing the performance of virtual desktops in distributed clouds','Design requirements of a global name service for a mobility- centric, trustworthy internetwork','Identifying and Addressing Protocol Manipulation Attacks in "Secure" BGP','On the CDN pricing game','Distributing content simplifies ISP traffic engineering'],
                    2012: ['MobilityFirst: a robust and trustworthy mobility-centric architecture for the future internet','Pros \\&amp;amp; Cons of Model-based Bandwidth Control for Client-assisted Content Delivery', 'Distributing Content Simplifies ISP Traffic Engineering'],
                    2011: ['Anticipatory Wireless Bitrate Control for Blocks','R3: Robust Replication Routing in Wireless Networks with Diverse Connectivity Characteristics','ZZ and the Art of Practical BFT Execution','Beyond MLU: An Application-Centric Comparison of Traffic Engineering Schemes'],
                    2010: ['Disaster Recovery as a Cloud Service: Economic Benefits & Deployment Challenges','Contracts: Practical contribution incentives for P2P live streaming','Replication routing DTNs: A resource allocation approach','Estimating self-sustainability in peer-to-peer swarming systems','Augmenting mobile 3G using WiFi', 'Information plane for determining performance metrics of paths between arbitrary end-hosts on the internet'],
                    2009: ['Content Availability and Bundling in Peer-to-Peer Swarming Systems','Energy Consumption in Mobile Phones: A Measurement Study and Implications for Network Applications','Modeling Chunk Availability in P2P Swarming Systems','Modeling Content Availability in Peer-to-Peer Swarming Systems','iPlane Nano: Path Prediction for Peer-to-Peer Applications','Block-switched Networks: A New Paradigm for Wireless Transport','Sandpiper: Black-box and Gray-box Resource Management for Virtual Machines'],
                    2008: ['Enhancing Interactive Applications in Hybrid Networks','Interactive WiFi Connectivity From Moving Vehicles','Consensus Routing: The Internet as a Distributed System'],
                    2007: ['Multi-User Data Sharing in Radar Sensor Networks','Web Search from a Bus','DTN Routing as a Resource Allocation Problem','Availability in BitTorrent Systems','A Multipath Background Network Architecture','Black-box and Gray-box Strategies for Virtual Machine Migration','Do Incentives Build Robustness in BitTorrent?','A Comparison of DAG Scheduling Strategies for Internet-Based Computing','Safe Speculative Replication','Building Bit-Tyrant, a (more) strategic BitTorrent client','iPlane: Measurements and query interface'],
                    2006: ['iPlane: An Information Plane for Distributed Services','Online Hierarchical Cooperative Caching','A Structural Approach to Internet Path Latency','PRACTI Replication','Oasis: An Overlay-Aware Network Stack','A Comparison of Dag-Scheduling Strategies for Internet-Based Computing'],
                    2005: [],
                    2004: ['Mechanisms and Algorithms for Large-Scale Replication Systems','Online Hierarchical Cooperative Caching'],
                    2003: ['Separating Agreement from Execution for Byzantine Fault Tolerant Services','A Non-Interfering Deployable Web Prefetching System','Towards a Practical Approach to Confidential Byzantine Fault-Tolerance'],
                    2002: ['TCP Nice: A Mechanism for Background Transfers','Operating System Support for Massive Replication','Potential Costs and Benefits of Long-Term Prefetching for Content Distribution','Byzantine fault-tolerant confidentiality'],
                    2001: ['Bandwidth Constrained Placement in a WAN','Potential Costs and Benefits of Long-Term Prefetching for Content Distribution','Model Checking a Parameterized Directory-based Cache Coherence Protocol'],
                    2000: [],
                    1999: ['Conformance Testing of Protocols Represented as Communicating Finite State Machines'],
  }
  titles = [pub.title for pub in year_entry]
  assert len(check_entries[yr]) == len(year_entry), "%s has more than the expected entries, please check and update this test"%(yr)
  for pub_entry_item in check_entries[yr]:
    # print pub_entry_item==year_entry[0].title
    # print pub_entry_item, titles
    # print check_entries[2016][0]
    # print titles
    found = False
    for entry in titles:
      print entry
      print pub_entry_item
      if(entry == pub_entry_item):
        found = True
        break;
    assert found, "%s not present in the list for year : %d in %s"%(pub_entry_item, yr, str(titles))

if(len(sys.argv)>1 and sys.argv[1] == "fetch_gs"):
  save_publications_from_google_scholar()
  exit()

print("Generating File for Publications")

# def main():
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
            x = Publications(entry_type(i['ENTRYTYPE']))
            x.title = process_text(i['title'])
            
            i['title'] = process_text(i['title'])
            x.author = process_text(i['author'])
            i['author'] = process_text(i['author'])
            x.entry = i
            x.conference_name = conference_type(x.entry)
            if(not 'year' in i):
                print "YEAR IS MISSING FOR "
                print i
            x.year = int(i['year'])
            if('month' in i):
                x.month = i['month']
            if(x.year > max_year):
                max_year = x.year
            if(x.pub_type == "conference"):
                if(check_if_unique(conferences+journals+workshops, x)):
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
                if(check_if_unique(journals+conferences+workshops, x)):
                    journals.append(x)
                    entries.append(x)
            if(x.pub_type == "workshop"):
                if(check_if_unique(journals+conferences+workshops, x)):
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

new_gs_entries = add_google_scholar_entries(entries)
populate_abstract(entries)
non_year_entries = []
for gs_entry in new_gs_entries:
  if(gs_entry.year == None):
    non_year_entries.append(gs_entry)

years_entries =[]
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
target = open("year_publications.html", 'w')

yr = max_year
for year_entry in years_entries:
    s = ""
    for entry in year_entry:
      if(entry.google_scholar == True or re.search("SELECT",entry.entry["catteggory"])):
          s+= "<li>%s</li><br/>" %((entry.print_publication()))
    if(len(year_entry)>0):
        check_entries = [entry for entry in year_entry if(entry.google_scholar == True or re.search("SELECT",entry.entry["catteggory"]))]
        assert_years_entries(yr, check_entries)
        header = "<h5>%s</h5>" %(yr)    
        target.write(header+"<ul>"+s+"</ul>")
    yr-=1
s=""
for entry in non_year_entries:
  if(entry.google_scholar == True or re.search("SELECT",entry.entry["catteggory"])):
          s+= "<li>%s</li><br/>" %((entry.print_publication()))
if(len(non_year_entries)>0):
    header = "<h5>%s</h5>" %("Others")    
    target.write(header+"<ul>"+s+"</ul>")
target.close()



conference_publications(entries)
generate_publications_content('publications_content.html')


# if __name__ == "__main__":
#   main()
