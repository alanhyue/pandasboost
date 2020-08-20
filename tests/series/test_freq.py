from pandasboost.series.freq import freq
import pandasboost
import pandas as pd
from pandas.testing import assert_series_equal, assert_index_equal

def assert_series_value_equal(srs, lst):
    assert srs.tolist() == lst

def test_can_access_freq_in_booster():
    assert pd.Series.bs.freq is not None


def test_basic_usage():
    srs = pd.Series([1,1,2,3,3,3])
    freq = srs.bs.freq(business=False)
    print(freq)
    assert_series_value_equal(freq.index, [3,1,2])
    assert_series_value_equal(freq['freq'], [3,2,1])
    assert_series_value_equal(freq['pct'], [3/6,2/6,1/6])

