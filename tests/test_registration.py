import pytest
from pandasboost.registration import register_dataframe_booster


def test_register_dataframe_booster():
    import pandas as pd

    @register_dataframe_booster("redundant_shape")
    def redundant_shape(frame):
        return frame.shape

    assert hasattr(pd.DataFrame.bs, "redundant_shape")

