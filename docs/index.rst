.. pytest-portion documentation master file, created by
   sphinx-quickstart on Thu Oct  1 00:43:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytest-portion's documentation!
==========================================

`pytest-portion` is a pytest plugin that allows you to easily run a specific subset of your test suite.
This is particularly useful for parallelizing CI builds without complex orchestration.

Usage
-----

The plugin provides two primary modes of operation.

1. Test-Level Slicing (Default)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the plugin collects all tests and then slices the collected items.

.. code-block:: bash

    # Run the first half of all collected tests
    pytest --portion 1/2

    # Run tests in a specific percentage range
    pytest --portion 0.5:1.0

2. File-Level Slicing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a very large number of test files, collection itself can be slow. Use ``--portion-files``
to slice the list of files *before* pytest starts looking inside them.

.. code-block:: bash

    # Portion the files to accelerate collection
    pytest --portion 1/2 --portion-files

How it Works
------------

.. list-table:: Comparison
   :widths: 25 75
   :header-rows: 1

   * - Mode
     - Behavior
   * - **Default**
     - Collects everything, then deselects tests. Best for even distribution of parametrized tests.
   * - **Portion Files**
     - Scans the directory, slices the file list, and ignores files not in the portion. Best for speeding up collection in huge repos.



Configuration
-------------

The ``--portion`` argument accepts two formats:

* **Fractional:** ``i/n`` (where ``i`` is the 1-indexed slice number and ``n`` is total slices).
* **Percentage:** ``start:end`` (where ``start`` and ``end`` are floats between 0 and 1).

Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`