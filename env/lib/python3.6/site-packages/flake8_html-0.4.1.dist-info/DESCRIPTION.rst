===========
flake8-html
===========


.. image:: https://img.shields.io/pypi/v/flake8-html.svg
        :target: https://pypi.python.org/pypi/flake8-html

.. image:: https://img.shields.io/travis/lordmauve/flake8-html.svg
        :target: https://travis-ci.org/lordmauve/flake8-html

.. image:: https://pyup.io/repos/github/lordmauve/flake8-html/shield.svg
     :target: https://pyup.io/repos/github/lordmauve/flake8-html/
     :alt: Updates


A flake8 plugin to generate HTML reports of flake8 violations.

Simply

.. code-block:: bash

   $ pip install flake8-html

Then run flake8 passing the ``--format=html`` option and a ``--htmldir``:

.. code-block:: bash

   $ flake8 --format=html --htmldir=flake-report


Screenshots
-----------

Report index page:

.. image:: https://github.com/lordmauve/flake8-html
           /raw/master/screenshots/report-index.png

Per-file report, grouped by error code:

.. image:: https://github.com/lordmauve/flake8-html
           /raw/master/screenshots/file-report.png

Annotated, syntax-highlighed source code:

.. image:: https://github.com/lordmauve/flake8-html
           /raw/master/screenshots/annotated-source.png


License
-------

* Free software: Apache Software License 2.0

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.4.1 (2020-05-13)
------------------

* Fix: add compatibility with flake8 3.8.*

0.4.0 (2017-07-06)
------------------

* New: Add ``--htmlpep8`` option to produce normal flake8 console output
* Fix: Allow all ``flake8-html`` settings to be read from flake8 config


0.3.0 (2017-05-24)
------------------

* New: Add ``--htmltitle`` option to set page title


0.2.0 (2017-03-06)
------------------

* New: use SVG icons instead of Unicode characters
* New: deduplicate the same error on the same line


0.1.1 (2017-03-02)
------------------

* Fix: missing templates in sdist.


0.1.0 (2017-03-01)
------------------

* First release on PyPI.


