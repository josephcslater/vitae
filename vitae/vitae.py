import bibtexparser
from bibtexparser.bparser import BibTexParser
import os

def makemycv(filename = 'cv.bib', 
             silent = False, 
             entrytypes = ('inbook', 'article', 'periodical', 'techreport', 'inproceedings'),
             writeout = True, 
             indent = '   '): 
    """https://nwalsh.com/tex/texhelp/bibtx-7.html"""
    
    if os.path.isfile(filename) == False:
        print('{} is not an actual bib file.')
    
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False
 
    with open(filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    bibs = bib_database.entries

    results = {}
    for entrytype in entrytypes:
        entry = [[bib['year'], bib['ID'], bib['title']] for bib in bibs if bib['ENTRYTYPE'] == entrytype]

        entry_sorted = sorted(entry, key=lambda paper: paper[0], reverse = True)

        if silent == False:
            if entrytype[-1] =='s':
                print('Number of {} is {}'.format(entrytype, len(entry_sorted)))
            else:
                 print('Number of {}s is {}'.format(entrytype, len(entry_sorted)))
               
        file_contents = '\\begin{enumerate}\n'
        for entry in entry_sorted:
            file_contents += indent + '\\item \\bibentry{' + entry[1] + '}\n'
        file_contents += '\\end{enumerate}'
        if writeout == True:
            file = open(entrytype + '.tex', 'w')

            file.write(file_contents)
            file.close()
        else:
            print(file_contents)
        
        results[entrytype] = file_contents

    unaccounted = [bib for bib in bibs if bib['ENTRYTYPE'] not in entrytypes]                    

    if silent == False:
        print('Unaccounted for entries is {}:'.format(len(unaccounted)))
        for bib in unaccounted:
            print(bib['ID'], 
                  '\n    ', bib['year'], 
                  '\n    ', bib['ENTRYTYPE'], 
                  '\n    ', bib['title'])
    
    return results, unaccounted
