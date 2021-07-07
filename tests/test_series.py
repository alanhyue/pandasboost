import pytest
import pandas as pd
from numpy import nan
from pandas.testing import assert_series_equal
from pandasboost.series import cut_groups, frequency


def test_cut_groups():
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [5])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=5", "1. <=5", "2. >5"]))


def test_cut_groups_left_edge_case():
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [1])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=1", "2. >1", "2. >1"]))


def test_cut_groups_pad_zeros_on_double_digit_numbers():
    srs = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    grps = cut_groups(srs, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(grps)
    expected = pd.Series(
        [
            "01. <=1",
            "02. <=2",
            "03. <=3",
            "04. <=4",
            "05. <=5",
            "06. <=6",
            "07. <=7",
            "08. <=8",
            "09. <=9",
            "10. <=10",
            "11. >10",
        ]
    )
    assert_series_equal(grps, expected)


def test_cut_groups_ignores_bin_value_less_than_min_value():
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [0, 5])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=5", "1. <=5", "2. >5"]))


def test_cut_groups_include_cutoff_value_in_the_bin():
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [3])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=3", "1. <=3", "2. >3"]))


def test_cut_groups_include_missing_values():
    srs = pd.Series([1, 3, nan, 10])
    grps = cut_groups(srs, [3])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=3", "1. <=3", "0. missing", "2. >3"]))


def test_cut_groups_include_customized_missing_values():
    s = "n/a"
    srs = pd.Series([1, 3, nan, 10])
    grps = cut_groups(srs, [3], missing=s)
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=3", "1. <=3", "0. %s" % s, "2. >3"]))


def test_cut_groups_empty_interval():
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [3, 5])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=3", "1. <=3", "3. >5"]))


def test_cut_groups_right_most_bin_larger_than_series_max():
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [3, 100])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. <=3", "1. <=3", "2. <=100"]))


def test_cut_groups_customized_bin_name():
    name = "3 or less"
    srs = pd.Series([1, 3, 10])
    grps = cut_groups(srs, [(3, name)])
    print(grps)
    assert_series_equal(grps, pd.Series(["1. %s" % name, "1. %s" % name, "2. >3"]))


def test_freq():
    srs = pd.Series([1, 1, 2, 3, 3, 3])
    expected_index = pd.Series([3, 1, 2])
    expected_freq = pd.Series([3, 2, 1], index=expected_index, name="freq")
    expected_pct = pd.Series([3 / 6, 2 / 6, 1 / 6], index=expected_index, name="pct")

    freq = frequency(srs, business=False)
    print(freq)
    assert_series_equal(freq["freq"], expected_freq)
    assert_series_equal(freq["pct"], expected_pct)


def test_freq_by_index():
    srs = pd.Series([1, 1, 2, 3, 3, 3])
    expected_freq = pd.Series([2, 1, 3], index=pd.Series([1, 2, 3]), name="freq")

    freq = frequency(srs, by_index=True, business=False)

    assert_series_equal(expected_freq, freq["freq"])
