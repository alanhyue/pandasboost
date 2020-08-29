import pytest
from pandasboost.registration import register_dataframe_booster, register_series_booster


def test_register_dataframe_booster():
    import pandas as pd

    @register_dataframe_booster("redundant_shape")
    def redundant_shape(frame):
        return frame.shape

    assert hasattr(pd.DataFrame.bs, "redundant_shape")


def test_register_series_booster():
    import pandas as pd

    @register_series_booster("redundant_count")
    def count(srs):
        return srs.size()

    assert hasattr(pd.Series.bs, "redundant_count")

