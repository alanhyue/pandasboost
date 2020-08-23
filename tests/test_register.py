import pytest
import pandas as pd
from pandasboost import register


@pytest.mark.parametrize("name", ["levels", "drop", "keep"])
def test_access_dataframe_booster(name):
    df = pd.DataFrame()
    assert hasattr(df, "bs")
    assert hasattr(df.bs, name)
