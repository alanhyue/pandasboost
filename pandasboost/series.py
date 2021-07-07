import pandas as pd
from .registration import register_series_booster
from .formatter import bignum, format_percentage


@register_series_booster("cut_groups")
def cut_groups(srs, rules, right=True, missing="missing"):
    sample_item = rules[0]
    if isinstance(sample_item, (int, float)):
        bins = rules
        labels = ["<={}".format(c) for c in bins]
    elif isinstance(sample_item, tuple):
        bins = []
        labels = []
        for item in rules:
            bins.append(item[0])
            labels.append(item[1])
    _min = srs.min()
    if _min <= bins[0]:
        # set the min bin to min value minus 1 so the min value of the series is included in the minimum bin
        bins = [
            _min - 1,
        ] + bins
    else:
        labels = labels[1:]
    if right:
        largest_bin_cut = bins[-1]
        _max = srs.max()
        if _max > largest_bin_cut:
            bins.append(_max)
            if right == True:
                right_label = f">{largest_bin_cut}"
            else:
                right_label = right
            labels.append(right_label)
    if len(labels) >= 10:
        labelfmt = "{:02}. {}".format
    else:
        labelfmt = "{}. {}".format
    labels = [labelfmt(i + 1, v) for i, v in enumerate(labels)]
    cuts = pd.cut(srs, bins=bins, labels=labels, include_lowest=True)
    if missing is not None:
        groupnames = cuts.astype(str)
        missing_label = "0. {}".format(missing)
        groupnames = groupnames.replace("nan", missing_label)
    return groupnames


@register_series_booster("freq")
def frequency(srs, business=True, ascending=None, by_index=False):
    """
    Report frequency of values.

    Parameters
    ----------
    ascending: boolean, default None
        Whether to sort in ascending order. If none, will use ascending when sorted by index,
        and descending when sorted by frequency.
    by_index: boolean, default True
        Whether sort result by index.
    """
    c = srs.value_counts()
    c = c.to_frame("freq")
    c["pct"] = c / c["freq"].sum()
    if by_index:
        if ascending is None:
            ascending = True
        c = c.sort_index(ascending=ascending)
    else:
        if ascending is None:
            ascending = False
        c = c.sort_values(by="freq", ascending=ascending)
    c["cumfreq"] = c["freq"].cumsum()
    c["cumpct"] = c["pct"].cumsum()
    if business:
        formats = {
            "freq": bignum,
            "cumfreq": bignum,
            "pct": format_percentage,
            "cumpct": format_percentage,
        }
        for col, fmt in formats.items():
            c[col] = c[col].apply(fmt)
    c = c[["freq", "cumfreq", "pct", "cumpct"]]
    return c
