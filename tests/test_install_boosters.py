import pytest


def test_install_boosters():
    import pandas as pd
    from pandasboost import install_boosters

    assert hasattr(pd.DataFrame, "bs")
    assert hasattr(pd.Series, "bs")

