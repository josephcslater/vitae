
.. image:: http://pepy.tech/badge/vitae
   :target: http://pepy.tech/project/vitae
   :alt: PyPi Download stats

vitae
=====

A python module for building curriculum vitae and other documents from a ``bibtex`` file.

I hate formatting citations. It's tedious, and error-prone. Further, when I build my CV, I tend to muck it up and leave something out, mis-sort it, duplicate it accidentally, etc. So, I need a tool to do a better job.

The first function here, ``makemycv``, will take a few arguments and put sorted ``\bibentry`` commands into ``.tex`` files with names corresponding to `BibTeX entry <https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management#BibTeX>`_ types. In doing so, you can then simply use an ``\input`` command to embed all of these citations right in your document in an enumerated environment.

Right now, it only works for a ``bib`` file containing only papers of the CV-writer. I'll fix that eventually.

Eventually I'll put this on ``pypi``, but you can pip install it right now from github:

.. code::

  pip install git+https://github.com/josephcslater/vitae

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

Release notes:
--------------

0.1.1: You can now select only bibentries by a defined author. Note that authornames are not always all that unique. You need to ensure that all authornames are perfect for the selected author. That means initials, etc. I hope to use fuzzywuzzy for this someday- it's a bit complicated and a judgement call.  


Future plans
------------

1. Let LaTeX do formatting, then use (internally) pandoc_ to convert citations, and only citations, to any format you want- html, .docx, Markdown, etc.. I just need time to write some parsing scripts. This would have to check for pandoc_ and balk- leaving users without pandoc_ to get it installed.

2. Select only article by a specified author (could be a bit dangerous as names aren't as unique as one would think, and this could be error prone/difficult).

3. "dump formatted reverences", with a specificity on number and type.

What else would be nice?

.. _pandoc: http://pandoc.org
.. _texblog: https://texblog.org
.. _`Résumé in LaTeX`: https://texblog.org/2012/04/25/writing-a-cv-in-latex/
