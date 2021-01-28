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

- worker1: ``pytest tests/a``    (100 tests, ~4 minutes to finish)
- worker2: ``pytest tests/b``    (20 tests, ~1 minute to finish)
- worker3: ``pytest tests/c tests/d``  (30 tests, ~1 minute to finish)

The problem is that directory `tests/a` may have a lot more tests that `tests/c` plus `test/d`,
so ``worker1`` takes a lot more to finish.

With ``pytest-portion`` you can still split the tests in different instances, but letting
the extension makes the selection in a more balanced way.

- worker1: ``pytest --portion 1/3 tests``   (50 tests, ~2 minutes)
- worker2: ``pytest --portion 2/3 tests``   (50 tests, ~2 minutes)
- worker3: ``pytest --portion 3/3 tests``   (50 tests, ~2 minutes)

In this case, the tests of all the directories are collected, but only a third (a different one!) of them will
be actually executed on each worker.

Note this balance if **by number of tests**, so if there is very slow tests in a particular portion,
the duration may not be expected.

For a fine tuning, you could pass the portion in a more explicit way:

- worker1: ``pytest --portion 0:0.5 tests``    (first half, 1st to 75th test)
- worker2: ``pytest --portion 0.5:0.8 tests``  (next 30%, from 76th to 125º)
- worker3: ``pytest --portion 0.8:1 tests``    (last 20%)


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



Alternatively ``--portion start:end`` where:

- ``start`` and ``end`` are the coefficient (between 0 and 1) that represent the segment of the collected tests
to select.


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


Acknowledgements
----------------


- Thanks to ShipHero_ for give me some time to develop this.
- I used `cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template for the boilerplate code of this package. Thanks!


.. _`ShipHero`: https://www.shiphero.com
.. _`cookiecutter`: https://github.com/audreyr/cookiecutter
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
