# -*- coding: utf-8 -*-
import pytest
from pytest_portion import slice_fraction, slice_percentage_range


@pytest.mark.parametrize(
    "args, expected",
    [
        (("abc", 1, 7), ""),
        (("abc", 7, 7), "abc"),
        (("abc", 1, 1), "abc"),
        (("abcdefghi", 1, 2), "abcd"),
        (("abcdefghi", 2, 2), "efghi"),
        (("abcdefghi", 1, 3), "abc"),
        (("abcdefghi", 2, 3), "def"),
        (("abcdefghi", 3, 3), "ghi"),
        ((list("abcdefghijk"), 5, 5), ["i", "j", "k"]),
    ],
)
def test_slice_fraction(args, expected):
    assert slice_fraction(*args) == expected


@pytest.mark.parametrize(
    "seq, args, expected",
    [
        ("abc", (0, 0.333), "a"),
        ("abc", (0.333, 0.666), "b"),
        ("abc", (0.666, 1), "c"),
        ("abc", (0, 1), "abc"),  # all
        ("abcd", (0, 0.499), "ab"),
        ("abcd", (0.5, 1), "cd"),
        ("abcde", (0, 0.5), "abc"),  # c is repeated
        ("abcde", (0.5, 1), "cde"),
        ("abcdefghijk", (0, 0.5), "abcdef"),
        ("abcdefghijk", (0.5, 1), "ghijk"),
    ],
)
def test_slice_percentage(seq, args, expected):
    assert seq[slice_percentage_range(seq, *args)] == expected


@pytest.mark.parametrize(
    "portion, selected, expected",
    [
        ("1/3", ["Messi"], "1 passed, 3 deselected"),
        ("2/3", ["Ronaldo"], "1 passed, 3 deselected"),
        ("3/3", ["Riquelme", "Gaitan"], "2 passed, 2 deselected"),

        ("0:0.24", ["Messi"], "1 passed, 3 deselected"),
        ("0.25:0.49", ["Ronaldo"], "1 passed, 3 deselected"),
        ("0.5:1", ["Riquelme", "Gaitan"], "2 passed, 2 deselected"),
    ],
)
def test_select_fraction(testdir, portion, selected, expected):
    """Make sure that our plugin works."""

    testdir.makepyfile(
        """
        import pytest

        # 4 tests in total
        @pytest.mark.parametrize("name", ["Messi", "Ronaldo", "Riquelme", "Gaitan",])
        def test_dummy(name):
            return name != "Maradona"

        """
    )
    result = testdir.runpytest("-v", "--portion", portion)
    for player in selected:
        result.stdout.fnmatch_lines(f"*{player}*")
    assert expected in result.outlines[-1]
