Changelog
=========

1.2.1: Fix broken installs caused by bibtexparser 2.x:

- Pin ``bibtexparser<2`` in dependencies. bibtexparser 2.0 removed the
  ``bibtexparser.bparser`` module that ``vitae`` relies on, so unpinned
  installs picked up the incompatible release and failed to import.

1.2.0: Modernized packaging:

- Migrated from ``setup.py``/``setup.cfg`` (distutils/legacy setuptools) to
  ``pyproject.toml`` with the ``hatchling`` build backend. Version is still
  sourced from ``vitae/__init__.py``.
- Removed ``setup.py`` and ``setup.cfg``.
- Added GitHub Actions workflows:  ``.github/workflows/test.yml`` runs the
  test suite on push/PR across supported Python versions, and
  ``.github/workflows/publish.yml`` builds and publishes to PyPI via
  Trusted Publishing (OIDC) whenever a ``v*`` tag is pushed, removing the
  need for manually managed API tokens during release.
- Updated ``Makefile`` release targets accordingly.

1.1.4: Bug fixes and hardening:

- Fixed ``write_bibs`` default ``bibtex_types=('articles')``, which was a
  string rather than a tuple, causing entry-type filtering to match
  individual characters instead of whole entry types.
- ``makemycv`` now uses a ``with`` block when writing ``.tex`` files so the
  file handle is always closed, even on error.
- Replaced ``os.system`` calls (``lualatex``, ``bibtex``, ``pandoc``) with
  ``subprocess.run`` using argument lists. This avoids shell-quoting/
  injection issues with file paths and surfaces a warning if any of these
  external tools fail instead of failing silently.

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

.. _pandoc: http://pandoc.org
.. _luatex: http://www.luatex.org
