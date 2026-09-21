Releasing vitae
================

This document describes how to cut a new release of ``vitae`` and publish it
to PyPI_.

Overview
--------

Since 1.2.0, releases are built and published automatically by GitHub
Actions using `PyPI Trusted Publishing`_ (OIDC). There are no PyPI API
tokens to manage locally.

- ``.github/workflows/test.yml`` runs ``pytest`` (including doctests) on
  every push/PR to ``master`` across supported Python versions.
- ``.github/workflows/publish.yml`` builds the sdist/wheel and publishes to
  PyPI whenever a tag matching ``v*`` is pushed.

Release steps
-------------

1. Make sure ``master`` is green (check the "Tests" workflow in the
   `Actions tab`_).
2. Bump the version in ``vitae/__init__.py`` (``__version__ = 'X.Y.Z'``).
   ``pyproject.toml`` reads this value automatically via
   ``[tool.hatch.version]``; there is nothing else to bump.
3. Add an entry at the top of ``CHANGELOG.rst`` describing the release.
4. Commit and push to ``master``::

     git add -A
     git commit -m "Release X.Y.Z"
     git push origin master

5. Tag the release and push the tag. This triggers ``publish.yml``::

     git tag vX.Y.Z
     git push origin vX.Y.Z

6. Watch the "Publish to PyPI" run in the `Actions tab`_. On success the new
   version appears at https://pypi.org/project/vitae/.

``make release`` runs the tag/push steps (1-5 must already be done first);
see the ``Makefile`` for details.

PyPI Trusted Publishing setup
------------------------------

This only needs to be done once (already configured as of 1.2.1), and again
if the workflow file is renamed/moved or the environment name changes.

On https://pypi.org/manage/project/vitae/settings/publishing/, add a
publisher with **exactly**:

- Owner: ``josephcslater``
- Repository name: ``vitae``
- Workflow name: ``publish.yml`` (just the filename, not the full path)
- Environment name: ``pypi``

These must match the ``environment:`` block in
``.github/workflows/publish.yml`` exactly, or PyPI will reject the OIDC
token exchange with an ``invalid-publisher`` error. If that happens, re-check
each of the four fields above (owner/repo casing, workflow filename with no
path prefix, environment name) against the workflow file and try again.

Building locally (without publishing)
--------------------------------------

To build the sdist/wheel locally, e.g. to inspect contents or install from
git-adjacent files without dependencies on GitHub Actions::

  python -m pip install --upgrade build twine
  python -m build
  python -m twine check dist/*

.. _PyPI: https://pypi.org/project/vitae/
.. _`PyPI Trusted Publishing`: https://docs.pypi.org/trusted-publishers/
.. _`Actions tab`: https://github.com/josephcslater/vitae/actions
