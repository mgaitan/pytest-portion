# pytest-portion

[![CI](https://github.com/mgaitan/pytest-portion/actions/workflows/ci.yml/badge.svg)](https://github.com/mgaitan/pytest-portion/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/pytest-portion.svg)](https://pypi.org/project/pytest-portion)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-portion.svg)](https://pypi.org/project/pytest-portion)
[![Changelog](https://img.shields.io/github/v/release/mgaitan/pytest-portion?include_prereleases&label=changelog)](https://github.com/mgaitan/pytest-portion/releases)
[![docs](https://img.shields.io/badge/docs-blue.svg?style=flat)](https://mgaitan.github.io/pytest-portion/)


Select a portion of the collected tests, so you can run different parts of your test suite
in different instances to scale horizontally.

## Use case

Suppose you have a big, slow test suite, but you can trigger several CI workers
to run different portions of it, in a sake lazy/simple way to parallelize it.

A basic, obvious way to do that is to explictily
collect from different directories/modules:

- worker1: `pytest tests/a` (100 tests, ~4 minutes to finish)
- worker2: `pytest tests/b` (20 tests, ~1 minute to finish)
- worker3: `pytest tests/c tests/d` (30 tests, ~1 minute to finish)

The problem is that directory `tests/a` may have a lot more tests that `tests/c` plus `test/d`,
so `worker1` takes a lot more to finish.

With `pytest-portion` you can still split the tests in different instances, but letting
the extension makes the selection in a more balanced way.

- worker1: `pytest --portion 1/3 tests` (first 50 tests, ~2 minutes)
- worker2: `pytest --portion 2/3 tests` (next 50 tests, ~2 minutes)
- worker3: `pytest --portion 3/3 tests` (last 50 tests, ~2 minutes)

In this case, the tests of all the directories are collected, but only a third (a different one!) of them will
be actually executed on each worker.

Note this balance is **by number of tests**, so if there is very slow tests in a particular portion,
the duration may not be expected.

For a fine tuning, you could pass the portion in a more explicit way:

- worker1: `pytest --portion 0:0.5 tests` (first half, 1st to 75th test)
- worker2: `pytest --portion 0.5:0.8 tests` (next 30%, from 76th to 125th)
- worker3: `pytest --portion 0.8:1 tests` (last 20%)

## Installation

You can add "pytest-portion" to your project from [PyPI](https://pypi.org/project/pytest-portion/) with [uv](https://docs.astral.sh/uv/).

```bash
uv add --dev pytetest-portion
```

Or via [pip]

```bash
pip install pytest-portion
```

## Usage

There are two modes of operation: **Test-level** (default) and **File-level**.

### 1. Test-level Slicing (Default)

Pytest collects all tests first, then `pytest-portion` filters them.

Pass `--portion <i/n>` where:

- `n` is the total number of portions.
- `i` is the i-th portion to select (`1 <= i <= n`).

> **Note:**
> If the number of tests collected is not divisible by `n`, the last portion will contain the rest.
> For instance, if you have `test_1`, `test_2` and `test_3`, `--portion 1/2` will run the first one,
> and `--portion 2/2` the last 2.

Alternatively, use `--portion start:end` where `start` and `end` are coefficients between 0 and 1.

### 2. File-level Slicing

For very large projects, collection itself can be slow. Use `--portion-files` to slice the list of
discovered files **before** pytest starts collecting tests from within them. This can significantly
reduce collection time in large repositories.

```bash
# Collect and run only the files belonging to the first half of the suite
pytest --portion 1/2 --portion-files tests/
```

## Contributing

Contributions are very welcome. Please ensure the coverage at least stays
the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license, "pytest-portion" is free and open source software.

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## Acknowledgements

I used [cookiecutter] along with [@hackebrot]'s [cookiecutter-pytest-plugin] template for the boilerplate code of this package. Thanks!

[cookiecutter]: https://github.com/audreyr/cookiecutter
[@hackebrot]: https://github.com/hackebrot
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
[file an issue]: https://github.com/mgaitan/pytest-portion/issues
[pytest]: https://github.com/pytest-dev/pytest
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/project
