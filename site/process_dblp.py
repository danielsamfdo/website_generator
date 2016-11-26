f = open('dblp.bib', 'r')
main_file = open('main_dblp.bib','w')
for i in f.readlines():
    if(i=="}\n"):
        main_file.write('  catteggory = "SELECT Network",\n')# TO ADD A CATTEGGORY TO THE FILE
    main_file.write(i)
main_file.close()
f.close()
