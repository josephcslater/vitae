import bibtexparser
import tempfile
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

    an = authorname.replace(" ", "")

    authorname = authorname.replace(',', ', ')
    authorname = authorname.replace("  ", " ")

    authorshort = 'xxxxxxx'
    if ',' in authorname and len(an) > (1+an.find(',')):
        authorshort = (authorname[:authorname.find(',')]
                       + ', '
                       + an[an.find(',')+1])

    for bib in bibs:

        if 'author' in bib:
            bibauthor = bib['author']
            bibauthor = bibauthor.replace(',', ', ')
            bibauthor = bibauthor.replace('  ', ' ')

            if authorname in bibauthor:
                keepindex.append(i)
                i += 1
            elif authorshort in bibauthor:
                print('Close name WARNING- is bib entry correct?')
                print(bib['author'], ': ', bib['title'])
    author_bibs = [bibs[i] for i in keepindex]
    return author_bibs


def replace_enquote(string):
    r"""Replace \enquote with proper quotes."""
    front = string[:string.find(r'\enquote{')]
    back = string[string.find(r'\enquote{'):].replace('}', "''", 1)
    back = back.replace(r'\enquote{', '``')
    return front + back


def read_bbl(bblfilename):
    """Read bbl file and return dictionary of formatted citations."""
    if not is_tool('pdflatex') or not is_tool('bibtex'):
        print("Both pdflatex and bibtex must exist on your command",
              " line to use this function.")
        return

    isbibtext = 0
    formattedbibs = {}
    with open(bblfilename) as bbl:
        for line in bbl:
            if line[:6] == r'\begin' or line[:4] == r'\end':
                pass
            elif r'\providecommand' in line:
                pass
            elif r'bibitem' in line:
                bibitem = line[line.find('{')+1: line.find('}')]
                isbibtext = 1
                bibtext = ''
            elif isbibtext == 1:
                if len(line) > 2:
                    bibtext += line.strip('\n')
                elif len(line) < 2:
                    bibtext = replace_enquote(bibtext)
                    formattedbibs[bibitem] = bibtext
                    isbibtext = 0

    return formattedbibs


def formatted_bibs(bibfile, bibliographystyle='plain'):
    """Make a dictionary of formatted bibs.

    Parameters
    ----------
    bibfile : string
        full path and file name to the .bib file
    bibliographystyle : string (optional)
        bst (bib style file) to use. Default: 'plain'

    Returns
    -------
    formattedbibs : dictionary of strings
        dictionary of formatted citations with Cite keys as keys.

    """
    path = os.path.dirname(bibfile)
    os.path.basename(bibfile)

    bibliographystyle = bibliographystyle.replace('.bst', '')

    with tempfile.TemporaryDirectory() as tmpdirname:
        old_directory = os.getcwd()
        with open(os.path.join(tmpdirname, 'cv_temp.tex'), 'w') as template:
            # template_head = 'string'
            # print(bibfile)
            template_head = (r"""% !TEX root = cv.tex
            \documentclass[12pt, letter]{article}
            \usepackage[utf8]{inputenc}
            \usepackage[T1]{fontenc}
            \usepackage{bibentry}
            \newcommand{\enquote}[1]{``#1''}
            \makeatletter\let\saved@bibitem\@bibitem\makeatother
            \usepackage[colorlinks=true]{hyperref}
            \makeatletter\let\@bibitem\saved@bibitem\makeatother
            \usepackage{url}{}
            \renewcommand{\cite}{\bibentry}
            \begin{document}
            \nobibliography{"""
            + bibfile
            + r"""}
            \bibliographystyle{"""
            + bibliographystyle
            + r"""}
            \pagestyle{plain}
            \input{article.tex}
            \input{inbook.tex}
            \input{inproceedings}
            \input{periodical}
            \input{techreport}
            \end{document}""")
            template.write(template_head)

        os.chdir(tmpdirname)
        makemycv(filename=bibfile, silent=True)
        os.system("pdflatex cv_temp")
        os.system("bibtex cv_temp")
        formattedbibs = read_bbl(os.path.join(tmpdirname, 'cv_temp.bbl'))
        os.chdir(old_directory)
    return formattedbibs


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None
