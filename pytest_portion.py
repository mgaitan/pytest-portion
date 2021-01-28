# -*- coding: utf-8 -*-


def pytest_addoption(parser):
    group = parser.getgroup("portion")
    group.addoption(
        "--portion", action="store", help='Select a part of all the collected tests in the form "i/n" (1 <= i <= n)'
    )


def slice_fraction(sequence, i, n):
    """
    Split a sequence in `n` slices and then return the i-th (1-indexed).
    The last slice will be longer if the sequence can't be splitted even-sized or
    n is greater than the sequence's size.
    """
    total = len(sequence)

    per_slice = total // n

    if not per_slice:
        return sequence if i == n else type(sequence)()

    ranges = [[n, n + per_slice] for n in range(0, total, per_slice)]

    # fix last
    if total % n != 0:
        ranges = ranges[:-1]
        ranges[-1][1] = None

    portion = dict(enumerate(ranges, 1))[i]
    return sequence[slice(*portion)]


def pytest_collection_modifyitems(config, items):
    try:
        portion = config.getoption("portion") or config.getini("portion")
    except ValueError:
        portion = None

    if not portion:
        return

    i, n = [int(n) for n in portion.split("/")]

    selected = slice_fraction(items, i, n)
    for range_number in range(1, n + 1):
        if range_number == i:
            continue

        deselected = slice_fraction(items, range_number, n)
        config.hook.pytest_deselected(items=deselected)
    items[:] = selected
