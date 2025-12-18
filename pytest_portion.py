import pathlib

import pytest


portion_files = pytest.StashKey[list]()


def pytest_addoption(parser):
    group = parser.getgroup("portion")
    group.addoption(
        "--portion",
        action="store",
        help='Select a part of all the collected tests in the form "i/n" or "start:end"',
    )
    group.addoption(
        "--portion-files",
        action="store_true",
        default=False,
        help="Portion the discovered files instead of individual tests to accelerate collection.",
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


def pytest_sessionstart(session: pytest.Session) -> None:
    config = session.config
    if not config.getoption("--portion-files"):
        return

    portion_raw = config.getoption("--portion")
    if not portion_raw:
        return

    # 1. Gather all potential test files (matching pytest's default patterns)
    # We look in the arguments passed to pytest (e.g., 'pytest tests/')
    search_dirs = session.config.args or ["."]
    all_files = []
    for root in search_dirs:
        # Standard pytest discovery patterns for files
        all_files.extend(pathlib.Path(root).rglob("test_*.py"))
        all_files.extend(pathlib.Path(root).rglob("*_test.py"))

    # 2. Sort to ensure consistency across different workers/environments
    all_files = sorted(list(set(all_files)))

    # 3. Apply slicing logic
    try:
        if "/" in portion_raw:
            i, n = map(int, portion_raw.split("/"))
            selected_files = slice_fraction(all_files, i, n)
        elif ":" in portion_raw:
            start, end = map(float, portion_raw.split(":"))
            s = slice_percentage_range(all_files, start, end)
            selected_files = all_files[s]
        else:
            selected_files = all_files
    except (ValueError, IndexError):
        selected_files = all_files

    # 4. Store the "Allowed" list in the stash
    config.stash[portion_files] = [f.resolve() for f in selected_files]


def pytest_ignore_collect(collection_path: pathlib.Path, config: pytest.Config):
    allowed_files = config.stash.get(portion_files, None)
    if not allowed_files:
        return None

    portion_raw = config.getoption("--portion")
    if not portion_raw:
        return None

    resolved_path = collection_path.resolve()
    # 1. If it's a file, it must be in our allowed list
    if resolved_path.is_file():
        # Only apply ignore logic to python files to avoid ignoring conftest/ini
        if resolved_path.suffix == ".py":
            return resolved_path not in allowed_files
        return None

    # 2. If it's a directory, only allow it if it's a parent of an allowed file
    if resolved_path.is_dir():
        # Check if any allowed file starts with this directory path
        is_parent_of_allowed = any(
            allowed_file.as_posix().startswith(resolved_path.as_posix())
            for allowed_file in allowed_files
        )
        # Return True to IGNORE if it's NOT a parent of any allowed file
        return not is_parent_of_allowed


def pytest_collection_modifyitems(config, items):
    # Do not ignore tests if we already ignored the files
    if config.getoption("--portion-files"):
        return None

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
        deselected.extend(items[: slice_selected.start])
        deselected.extend(items[slice_selected.stop :])

    items[:] = selected
    config.hook.pytest_deselected(items=deselected)
