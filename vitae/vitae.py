import bibtexparser
import tempfile
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
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
    entrytypes : tuple of strings (optional)
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
    parser.customization = homogenize_latex_encoding
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

    return results, unaccounted, bibs


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
    # print(bibtexparser)
    bbl = open(bblfilename, "r")
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
    bibs : array
        bibfile array from bibtexparser

    """
    path = os.path.dirname(bibfile)
    bibfilename = os.path.basename(bibfile)

    bibliographystyle = bibliographystyle.replace('.bst', '')
    old_directory = os.getcwd()

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        with open('cv_temp.tex','w') as template:
            # template.write('hello')
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
            _, _, bibs = makemycv(filename=bibfile, silent=True)
        os.system("pdflatex cv_temp; bibtex cv_temp")

        # print(os.path.join(tmpdirname, 'cv_temp.bbl'))
        formattedbibs = read_bbl('cv_temp.bbl')

        os.chdir(old_directory)  # Unnecessary
    return formattedbibs, bibs


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None


def merge_formatted_into_db(formattedbibs, bibfilename=None, bibs=None):
    """Create bib database including formated bibs."""


    if bibs is None:
        if bibfilename is None:
            print('No bib file name given.')
            return

        if os.path.isfile(bibfilename) is False or 'bib' not in bibfilename:
            print('{} is not an actual bib file.')
            return

        parser = BibTexParser()
        parser.ignore_nonstandard_types = False

        with open(bibfilename) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file, parser)

        bibs = bib_database.entries

    bib_database = [[bib['year'],
                     bib['ID'],
                     bib['title'],
                     bib['ENTRYTYPE'],
                     formattedbibs[bib['ID']]]
                    for bib in bibs if bib['ID'] in formattedbibs.keys()]

    return bib_database


def write_bibs(bibfile=None,
               bibliographystyle='plain',
               outfile_name=None,
               since_year=None,
               number_citations=None,
               bibtex_type=('articles'),
               write_over=False,
               authorname=None,
               outputformat=None,
               silent=False,
               standalone=True,
               overwrite=False):
    """Write formatted bibs from bibfile to desired format.

    Parameters
    ----------
    bibfile : string
        full path and file name to the .bib file
    bibliographystyle : string (optional)
        bst (bib style file) to use. Default: 'plain'.
    outfile_name : string (optional)
        name of output file. Default bibfile name with .tex extension. Default
        output format is html.
    since_year : integer (optional)
        year of oldest citation to include. Default: All years.
    number_citations : integer (optional)
        maximum number of citations to include. Default: all.
    entrytypes : tuple of strings (optional)
        list of types of entries to include. Default: ('articles')
    authorname : string (optional)
        author whos papers to include. Default: all.
    silent : Boolean (optional)
        display diagnostics. Default: False (will display diagnostics)
    standalone : Boolean (optional)
        By default, pandoc generates only a fragment. If you want a full
        document set this to False. Default: True
    overwrite : Boolean (optional)
        Overwrite results files? Default: False

    """
    if '.bib' in outfile_name:
        print('I refuse to write over a bib file. '
              + 'While this software comes with no warrantee, '
              + "I'm also not going to knowlingly cause you damage. "
              + 'Please choose a more sensible output file name.')
        return

    if bibfile is None:
        print('You must include a bibfile path with full name.')
        print('')
        print('On Mac or Linux, this looks like:')
        print('\'/Users/myusername/Documents/CVs/cv.bib\'')
        print('')
        print('On Windows, this looks like:')
        print('r\'C:\\Users\\myusername\\Documents\\CVs\\cv.bib\'')
        print('NOTE: The \'r\' may be necessary on Windows so that '
              + '\'\\\' is not treated as an escape character.')
        return

    if os.path.isfile(bibfile) is False:
        print(bibfile, ' cannot be found at that location.')
        print('Please check path and try again.')
        return

    if (not is_tool('pdflatex')
            or not is_tool('bibtex')
            or not is_tool('pandoc')):

        print("pdflatex, bibtex and pandoc must exist on your command",
              " line to use this function.\n")
        print("Please see the documentation at:")
        print(r"https://github.com/josephcslater/vitae")
        return

    path = os.path.dirname(bibfile)
    bibfilename = os.path.basename(bibfile)
    bibfilenameroot = bibfilename[:-4]

    # No output file specified
    if outfile_name is None:
        outfile_name = bibfilenameroot + '.html'
        outfile_name = os.path.join(path, outfile_name)

    if os.path.dirname(outfile_name) is '':
        path_output = path
    else:
        path_output = os.path.dirname(outfile_name)

    if not os.path.isdir(path_output) and path_output is not '':
        print('Specified output path:')
        print(path_output)
        print('is not a valid path. Please play again.')
        return

    filename_output = os.path.basename(outfile_name)
    root_output = filename_output[:filename_output.find('.')]

    # Format the bibs. We just format every one in the file, then use what we
    # must later.
    formattedbibs, bibs = formatted_bibs(bibfile,
                                         bibliographystyle=bibliographystyle)

    bibs = merge_formatted_into_db(formattedbibs, bibs=bibs)

    # Keep only bibs by chosen author.
    if authorname is not None:
        bibs = by_author(authorname, bibs)

    # At this point, we have a bibs database with just bibs by authorname
    # Next steps:

    # 3. Truncate non-desired entrytypes
    bibs = [bib for bib in bibs if bib[3] in bibtex_type]

    # Sort by date
    bibs_sorted = sorted(bibs, key=lambda paper: paper[0], reverse=True)

    # 2. Truncate older articles
    if since_year is not None:
        bibs_truncated = [bib for bib in bibs_sorted if int(bib[0]) >= since_year]
    else:
        bibs_truncated = bibs_sorted

    # 4. Truncate beyond numberself.

    if number_citations is not None and number_citations < len(bibs_truncated):
        bibs_final = bibs_truncated[:number_citations]
    else:
        bibs_final = bibs_truncated

    cwd = os.getcwd()

    os.chdir(path_output)

    outfile_name_tex = root_output + '.tex'

    if os.path.isfile(outfile_name_tex) and not overwrite:
        os.rename(outfile_name_tex, outfile_name_tex[:-4]+'_old.tex')

    # routine to write out bibs_final bibsfinalfilename
    with open(outfile_name_tex, 'w') as filename:
        for bib in bibs_final:
            filename.write(bib[4])
            filename.write('\n')
            filename.write('\n')

    # Store old version of formatted references.
    if os.path.isfile(filename_output) and not overwrite:
        os.rename(filename_output,
                  filename_output[:filename_output.find('.')]
                  + '_old'
                  + filename_output[filename_output.find('.'):])

    if standalone:
        pandoc_args = ' -s '

    pandocstring = ("pandoc "
                    + pandoc_args
                    + outfile_name_tex
                    + " -o "
                    + filename_output)

    os.system(pandocstring)
    os.chdir(cwd)
    # 5. Write to file, but check if it exists and store it somehow.
    # 6. Apply pandoc
