
.. image:: http://pepy.tech/badge/vitae
   :target: http://pepy.tech/project/vitae
   :alt: PyPi Download stats

vitae
=====

A Python module for building curriculum vitae and other documents from a ``BibTeX`` file. ``vitae`` leverages bibtexparser_, `LaTeX`_, and pandoc_ to streamline getting citations of your papers into the formats you need quickly without manual intervention. Of course, with many settings, it can be a bit tedious. I personally recommend setting up a Jupyter_ notebook with the commands you regularly execute available there. Alternatively, you can call it from the terminal which allows it to work inside a more complex workflow.

Purpose
-------

I hate formatting citations. It's tedious, and error-prone. Further, when I build my CV, I tend to muck it up and leave something out, mis-sort it, duplicate it accidentally, etc. So, I need a tool to do a better job with what ie a menial task.

Install
-------

.. code::

  pip install vitae

or

.. code::

   pip install --user vitae

Usage
-----

Please see the brief `demo Jupyter notebook`_. It's very brief. I need to add more. The whole package is basically two functions. Please read the help:

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

Then, with your maintained `.bib` file, in the same location as your cv (for now), and **within the same directory as your cv and cv.bib file** open a python terminal and type.

.. code::

  >>> import vitae
  >>> vitae.makemycv()

Alternatively, you can type::

  > python -c  "import vitae; vitae.makemycv()"

in your terminal (Anaconda Terminal if you are using Anaconda Python on Windows).

This will make your ``article.tex`` file along with the other defaults (see the help on ``makemycv``).

Note that that are a ton of options for ``makemycv``. Please use::

  >>> import vitae
  >>> help(vitae.makemycv)

To see how to tweak it to your needs.

If you try ``vitae``, please understand:

a. No warrantee. This is still a work in progress.
b. Please provide your feedback.
c. Please help! I can use help with additional portions.

If you don't use LaTeX, this isn't easy enough for you yet. It's a long ways away. However, texblog_ has a decent start in writing a `Résumé in LaTeX`_ . It *doesn't* include the paper inclusion trick being used by ``vitae``.

``write_bibs``
~~~~~~~~~~~~~~

The second function is ``write_bibs``. This allows you to convert bibs with a bunch of constraints into a format that pandoc_ can output. It REQUIRES a full `LaTeX`_ and pandoc_ installation that works in your terminal environment.

Constraints include:

1. Since a year
2. Number
3. Types of publications

For instance:

.. code::

  >>> import vitae
  >>> vitae.write_bibs(bibfile = '/Users/jslater/Documents/Resumes/cv.bib',
                       bibliographystyle='aiaa',
                       outfile_name='try.html',
                       since_year=2008)

Alternatively, from a command line::

  > python -c  "import vitae; vitae.write_bibs(bibfile='cv.bib',
                                               bibliographystyle='aiaa',
                                               outfile_name = 'bibs.html',
                                               since_year=2008)"

How I use it
------------

I have a Makefile that I use for tasks that I am creating. The first is a simple one for building my cv, the contents of which are::

	help:
		@echo "Please use \`make <target>' where <target> is one of"
		@echo "  cv         to make standard pdf cv"
		@echo "  pdf        see cv"

	cv:
			python -c  'import vitae; vitae.makemycv(silent = True)'
		  pdflatex cv
			bibtex cv
			pdflatex cv

	pdf:
			cv

Summary
-------
Please see the full help on each function.

Vitae is on pypi_ but you can pip install the latest, and possibly non-working, version right now from github (I love bug reports!):

.. code::

  pip install git+https://github.com/josephcslater/vitae

Help
----
``vitae`` uses luatex_ to enable unicode characters. On Ubuntu, the base tetex install doesn't include the necessary file ``luaotfload``. To resolve this open a terminal and type::

  sudo apt install texlive-luatex

Release notes:
--------------

1.1.3: Work-around for pandoc_ failure to convert ``{\em`` correctly.

1.1.2: Unify name of ``bibtex_types`` and ``entrytypes``. Will issue a warning
       if you incorrectly use ``entrytypes``, but will still work.

1.1.1: Included test bib file that can easily be accessed from notebook.
       Corrected incorrect help in ``makemycv``
       Minor non-functional corrections.

1.1.0: Numerous minor fixes:

- ``write_bibs`` failed when path not explicitly included.
- Quieted latex output.
- Moved to luatex_ to enable unicode characters.
- Readme updated to reflect terminal usage.

1.0.0: You can now convert your bib citations to any format that pandoc_ can handle. I think.

0.1.1: You can now select only ``bibentries`` by a defined author. Note that ``authornames`` are not always all that unique. You need to ensure that all ``authornames`` are perfect for the selected author. That means initials, etc. I hope to use fuzzywuzzy for this someday- it's a bit complicated and a judgement call.

0.1.0: First release. It works, it's useful, it's not done, but it does what I needed it for. You can now use \\input statements with bibentry instead of typing your own citations by hand.


Future plans
------------

1. Preferences.

  a. Reader (doesn't overwrite specified arguments)

  b. Writer (configurator on call or when it doesn't exist)

  c. Editor?

2. Bug fixes when I find them. Any other suggestions?

What else would be nice?

.. _pandoc: http://pandoc.org
.. _luatex: http://www.luatex.org
.. _texblog: https://texblog.org
.. _`Résumé in LaTeX`: https://texblog.org/2012/04/25/writing-a-cv-in-latex/
.. _`LaTeX`: https://www.latex-tutorial.com/installation/
.. _bibtexparser: https://bibtexparser.readthedocs.io/en/master/
.. _Jupyter: https://www.Jupyter.org
.. _Makefile: https://www.gnu.org/software/make/manual/html_node/Introduction.html
.. _`demo Jupyter notebook`: https://github.com/josephcslater/vitae/blob/master/Vitae.ipynb
.. _pypi: https://pypi.org/project/vitae/
