import pytest
import pandas as pd
from numpy import nan
from pandas.testing import assert_series_equal
import pandasboost

def test_dataframe_bs_accessor():
    assert pd.DataFrame.bs is not None

def test_Series_bs_accessor():
    assert pd.Series.bs is not None

def test_can_access_cut_groups():
    assert pd.Series.bs.cut_groups is not None

def test_cut_groups():
    srs = pd.Series([1, 3, 10])
    grps = srs.bs.cut_groups([5])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=5', '1. <=5', '2. >5']))

def test_cut_groups_ignores_bin_value_less_than_min_value():
    srs = pd.Series([1, 3, 10])
    grps = srs.bs.cut_groups([0, 5])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=5', '1. <=5', '2. >5']))

def test_cut_groups_include_cutoff_value_in_the_bin():
    srs = pd.Series([1, 3, 10])
    grps = srs.bs.cut_groups([3])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=3', '1. <=3', '2. >3']))

def test_cut_groups_include_missing_values():
    srs = pd.Series([1, 3, nan, 10])
    grps = srs.bs.cut_groups([3])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=3', '1. <=3', '0. missing', '2. >3']))

def test_cut_groups_include_customized_missing_values():
    s = 'n/a'
    srs = pd.Series([1, 3, nan, 10])
    grps = srs.bs.cut_groups([3], missing=s)
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=3', '1. <=3', '0. %s' %s, '2. >3']))

def test_cut_groups_empty_interval():
    srs = pd.Series([1, 3, 10])
    grps = srs.bs.cut_groups([3, 5])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=3', '1. <=3', '3. >5']))

def test_cut_groups_right_most_bin_larger_than_series_max():
    srs = pd.Series([1, 3, 10])
    grps = srs.bs.cut_groups([3, 100])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. <=3', '1. <=3', '2. <=100']))


def test_cut_groups_customized_bin_name():
    name = '3 or less'
    srs = pd.Series([1, 3, 10])
    grps = srs.bs.cut_groups([(3, name)])
    print(grps)
    assert_series_equal(grps, pd.Series(['1. %s' % name, '1. %s' % name, '2. >3']))

