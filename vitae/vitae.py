import bibtexparser
from bibtexparser.bparser import BibTexParser
import os


def makemycv(filename='cv.bib',
             silent=False,
             entrytypes=('inbook', 'article', 'periodical',
                         'techreport', 'inproceedings'),
             writeout=True,
             indent='   ',
             author=None):
    """Create sub-bib TeX files for including into CV.

    Parameters
    ----------
    filename : string (optional: default cv.tex)
        Name (including optional path) of bib file containing citation entries
    entrytypes : list of strings (optional)
        List of bibtex entrytypes to generate \\bibentry .tex files for.
        Files will be be named  `entrytype```.tex``
    writeout : boolean (optional: default True)
        Write to files. If false, only write to screenself.
    indent : string
        string of spaces for prettying up the item lists
    author : string (unimplemented)
        select authors whose entries should be included.

    https://nwalsh.com/tex/texhelp/bibtx-7.html

    """
    if os.path.isfile(filename) is False:
        print('{} is not an actual bib file.')
        return

    parser = BibTexParser()
    parser.ignore_nonstandard_types = False

    with open(filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    bibs = bib_database.entries

    if author is not None:
        bibs = by_author(author, bibs)

    results = {}

    for entrytype in entrytypes:
        entry = [[bib['year'], bib['ID'], bib['title']]
                 for bib in bibs if bib['ENTRYTYPE'] == entrytype]

        entry_sorted = sorted(entry, key=lambda paper: paper[0], reverse=True)

        if silent is False:
            if entrytype[-1] == 's':
                print('Number of {} is {}'.format(
                    entrytype, len(entry_sorted)))
            else:
                print('Number of {}s is {}'.format(
                    entrytype, len(entry_sorted)))

        file_contents = '\\begin{enumerate}\n'
        for entry in entry_sorted:
            file_contents += indent + '\\item \\bibentry{' + entry[1] + '}\n'
        file_contents += '\\end{enumerate}'
        if writeout is True:
            file = open(entrytype + '.tex', 'w')

            file.write(file_contents)
            file.close()
        else:
            print(file_contents)

        results[entrytype] = file_contents

    unaccounted = [bib for bib in bibs if bib['ENTRYTYPE'] not in entrytypes]

    if silent is False:
        print('Unaccounted for entries is {}:'.format(len(unaccounted)))
        for bib in unaccounted:
            print(bib['ID'],
                  '\n    ', bib['year'],
                  '\n    ', bib['ENTRYTYPE'],
                  '\n    ', bib['title'])

    return results, unaccounted


def by_author(authorname, bibs):
    """Return only bibs containing authorname."""
    keepindex = []
    i = 0
    for bib in bibs:

        if 'author' in bib and authorname in bib['author']:
            keepindex.append(i)
            i += 1
    author_bibs = [bibs[i] for i in keepindex]
    return author_bibs
