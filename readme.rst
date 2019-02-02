
.. image:: http://pepy.tech/badge/vitae
   :target: http://pepy.tech/project/vitae
   :alt: PyPi Download stats

vitae
=====

A Python module for building curriculum vitae and other documents from a ``bibtex`` file. ``vitae`` leverages bibtexparser_, `LaTeX`_, and pandoc_ to streamline getting citations of your papers into the formats you need quickly without manual intervention. Of course, with many settings, it can be a bit tedious. I personally recommend setting up a jupyter_ notebook with the commands you regularly execute available there. Alternatively, you can call it from scripts or create a Makefile_, I'll be doing both for myself.

Purpose
-------

I hate formatting citations. It's tedious, and error-prone. Further, when I build my CV, I tend to muck it up and leave something out, mis-sort it, duplicate it accidentally, etc. So, I need a tool to do a better job with what ie a menial task.

Usage
-----

``makemycv``
~~~~~~~~~~~~

To do anything useful here, you must have `LaTeX`_ with BibTeX installed. If you don't use `LaTeX`_, this module isn't the place to start. Sorry.

The first function here, ``makemycv``, will take a few arguments and put sorted ``\bibentry`` commands into ``.tex`` files with names corresponding to `BibTeX entry <https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management#BibTeX>`_ types. In doing so, you can then simply use an ``\input`` command to embed all of these citations right in your document in an enumerated environment.

You'll need the following in the header of your LaTeX cv file.

.. code::

  \usepackage{bibentry}
  \newcommand{\enquote}[1]{``#1''}
  \makeatletter\let\saved@bibitem\@bibitem\makeatother
  \usepackage[colorlinks=true]{hyperref}
  \makeatletter\let\@bibitem\saved@bibitem\makeatother

The last 3 lines are only necessary if you want to use the ``hyperref`` package, which has some compatibility issues with bibentry.

Then put:

.. code::

  \input{articles.tex}

where you want articles listed, etc.

Then, with your maintained .bib file, in the same location as your cv (for now), open a python terminal,

.. code::

  >>> import vitae
  >>> vitae.makemycv()

will make your ``article.tex`` file along with the other defaults (see the help on ``makemycv``).

If you try ``vitae``, please understand:

a. No warrantee. This is still a work in progress.
b. Please provide your feedback.
c. Please help! I can use help with additional portions.

If you don't use LaTeX, this isn't easy enough for you yet. It's a long ways away. However, texblog_ has a decent start in writing a `Résumé in LaTeX`_ . It *doesn't* include the paper inclusion trick being used by ``vitae``.

 "Other documents" is making some progress. It will look like zero until it's live because I'm adding partial functionality as I can (see github logs), but the whole thing is needed for it to be useful.

``write_bibs``
~~~~~~~~~~~~~~

The second function is ``write_bibs``. This allows you to convert bibs with a bunch of constraints into a format that pandoc_ can output. It REQUIRES a full `LaTeX`_ and pandoc_ installation that works in your terminal environment.

Constraints include:

1. Since a year
2. Number
3. Types of publications

For instance:

.. code::

  vitae.write_bibs(bibfile = '/Users/jslater/Documents/Resumes/cv.bib',
                    bibliographystyle='aiaa',
                    outfile_name='try.html',
                    since_year=2008)

Summary
-------
Please see the full help on each function.

It's on ``pypi``, but you can pip install the latest, and possibly non-working, version right now from github (I love bug reports!):

.. code::

  pip install git+https://github.com/josephcslater/vitae

Release notes:
--------------

1.0.0: You can now convert your bib citations to any format that pandoc_ can handle. I think.

0.1.1: You can now select only bibentries by a defined author. Note that authornames are not always all that unique. You need to ensure that all authornames are perfect for the selected author. That means initials, etc. I hope to use fuzzywuzzy for this someday- it's a bit complicated and a judgement call.

0.1.0: First release. It works, it's useful, it's not done, but it does what I needed it for. You can now use \\input statements with bibentry instead of typing your own citations by hand.


Future plans
------------

1. Bug fixes when I find them. Any other suggestions?

What else would be nice?

.. _pandoc: http://pandoc.org
.. _texblog: https://texblog.org
.. _`Résumé in LaTeX`: https://texblog.org/2012/04/25/writing-a-cv-in-latex/
.. _`LaTeX`: https://www.latex-tutorial.com/installation/
.. _bibtexparser: https://bibtexparser.readthedocs.io/en/master/
.. _jupyter: https://www.jupyter.org
.. _Makefile: https://www.gnu.org/software/make/manual/html_node/Introduction.html
