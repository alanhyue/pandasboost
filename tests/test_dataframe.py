import pytest
import pandas as pd
from pandasboost.dataframe import check_drop, check_keep, make_msg, check_merge


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


def test_check_merge(capsys):
    left = pd.DataFrame({"id": [1, 2, 3], "color": ["red", "blue", "red"],})
    right = pd.DataFrame({"id": [1, 2, 4], "size": [0.9, 0.1, 0.2],})
    expected_words = [
        "left",
        "right",
        "result",
        "%left matched",
        "%right matched",
        "3",
        "3",
        "3",
        "100%",
        "67%",
    ]

    check_merge(left, right, how="left", on="id", validate="1:1")

    stdout = capsys.readouterr().out
    for s in expected_words:
        assert s in stdout
