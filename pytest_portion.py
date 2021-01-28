# -*- coding: utf-8 -*-


def pytest_addoption(parser):
    group = parser.getgroup("portion")
    group.addoption(
        "--portion", action="store", help='Select a part of all the collected tests in the form "i/n" or "start:end"'
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


def slice_percentage_range(sequence, start, end):
    """
    return the slice range between coefficient `start` and `end`
    where start and end represents fractions between 0 and 1.

    Corner elements may be repeated in consecutive slices.
    """
    total = len(sequence)
    return slice(int(round(total * start)), int(total * end) + 1)


def pytest_collection_modifyitems(config, items):
    try:
        portion = config.getoption("portion") or config.getini("portion")
    except ValueError:
        portion = None

    deselected = []
    if not portion:
        return

    elif "/" in portion:

        i, n = [int(n) for n in portion.split("/")]

        selected = slice_fraction(items, i, n)
        for range_number in range(1, n + 1):
            if range_number == i:
                continue

            deselected.extend(slice_fraction(items, range_number, n))
    elif ":" in portion:
        start, end = [float(n) for n in portion.split(":")]

        slice_selected = slice_percentage_range(items, start, end)
        selected = items[slice_selected]
        deselected.extend(items[:slice_selected.start])
        deselected.extend(items[slice_selected.stop:])

    items[:] = selected
    config.hook.pytest_deselected(items=deselected)




