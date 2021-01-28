==============
pytest-portion
==============

.. image:: https://img.shields.io/pypi/v/pytest-portion.svg
    :target: https://pypi.org/project/pytest-portion
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-portion.svg
    :target: https://pypi.org/project/pytest-portion
    :alt: Python versions

.. image:: https://travis-ci.org/mgaitan/pytest-portion.svg?branch=master
    :target: https://travis-ci.org/mgaitan/pytest-portion
    :alt: See Build Status on Travis CI


Select a portion of the collected tests, so you can run diferents parts of your test suite
in differents instances to balance the number of test run on each one.

Use case
--------

Suppose you have a big, slow test suite, but you can trigger several CI workers
to run different portions of it, in a sake lazy/simple way to make it

A basic, obvious way to do that is to explictily
collect from different directories/modules

- worker1: ``pytest tests/a``
- worker2: ``pytest tests/b``
- worker3: ``pytest tests/c tests/d``

The problem is that directory `tests/a` may have a lot more tests that `tests/c` plus `test/d`,
so ``worker1`` takes, let say, 5 times more than ``worker3`` to finish.

With ``pytest-portion`` you can still split the tests in different instances, but letting
the extension makes the selection in a more balanced way.


- worker1: ``pytest --portion 1/3 tests``
- worker2: ``pytest --portion 2/3 tests``
- worker3: ``pytest --portion 3/3 tests``

In this case, the tests of all the directories are collected, but only a third (a different one!) of them will
be actually executed on each worker.


Installation
------------

You can install "pytest-portion" via `pip`_ from `PyPI`_::

    $ pip install pytest-portion


Usage
-----

Pass ``--portion <i/n>`` where:

- ``n`` is the number of portions
- ``i`` is the i-th portion to select (``1 <= i <= n``)

.. note::

    If the number of tests collected is not divisible by `n`, the last portion will contain the rest.
    For instance, if you have `test_1`, `test_2` and `test_3`, `--portion 1/2` will run the first one,
    and `--portion 2/2` the last 2.


Contributing
------------
Contributions are very welcome. Please ensure the coverage at least stays
the same before you submit a pull request.

License
-------

Distributed under the terms of the `BSD-3`_ license, "pytest-portion" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/mgaitan/pytest-portion/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
