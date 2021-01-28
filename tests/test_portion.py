# -*- coding: utf-8 -*-
import pytest
from pytest_portion import slice_fraction


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
    "portion, expected",
    [("1/3", "1 passed, 3 deselected"), ("2/3", "1 passed, 3 deselected"), ("3/3", "2 passed, 2 deselected"),],
)
def test_select_fraction(testdir, portion, expected):
    """Make sure that our plugin works."""

    testdir.makepyfile(
        """
        import pytest

        # 4 tests in total
        @pytest.mark.parametrize("name", ["Messi", "Ronaldo", "Riquelme", "Gaitán",])
        def test_dummy(name):
            return name != "Maradona"

        """
    )
    result = testdir.runpytest("--portion", portion)
    # result.assert_outcomes(passed=1)
    assert expected in result.outlines[-1]
