from bibtexparser.bparser import BibTexParser

with open('dblp.bib', 'r') as f:
    bfile = f
    bp = BibTexParser(bfile)
    entries = bp.get_entry_list()

# look at the first entry
print entries[0]