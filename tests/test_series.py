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

