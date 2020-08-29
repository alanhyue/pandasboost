import pytest
import pandas as pd
from pandasboost.dataframe import check_drop, check_keep, make_msg


def test_check_drop(capsys):
    shoes = pd.DataFrame(
        {"color": ["red", "green", "blue", "green"], "size": [7.8, 6, 7, 7],}
    )
    msk = shoes["color"] == "red"

    rst = check_drop(shoes, msk)

    assert 3 == rst.shape[0]
    out, err = capsys.readouterr()
    kwds = ["25%", "rows", "->"]
    for s in kwds:
        assert s in out


@pytest.mark.skip
def test_levels():
    raise NotImplementedError


@pytest.mark.skip
def test_missing():
    raise NotImplementedError
