from .registration import register_dataframe_booster
from .formatter import bignum, format_percentage
import pandas as pd
from functools import wraps


### Check / Drop rows
@register_dataframe_booster("keep")
def check_keep(frame, query, desc):
    """
    Filter a dataframe with `query` and report the number of rows affected.

    Parameters
    ----------
    query: str
        Query for filtering the dataframe. Will be passed to pandas.DataFrame.query.
    desc: str
        Description of the filter.
    """
    Sf = frame.shape[0]
    mf = frame.query(query).copy()
    Smf = mf.shape[0]
    Sm = Sf - Smf

    mPf = Smf / Sf
    msg = f"{mPf:.0%} ({Smf:,}) rows remain: {desc}."
    print(msg)
    return mf


@register_dataframe_booster("drop")
def check_drop(frame, mask):
    Sf = frame.shape[0]
    Sm = mask.sum()
    mf = frame.loc[~mask].copy()
    Smf = mf.shape[0]
    msg = make_msg(Sf, Sm, Smf, "dropped", mask.name)
    print(msg)
    return mf


def make_msg(Sf, Sm, Smf, action, desc):
    mPf = Sm / Sf
    return f"{mPf:.0%} ({Smf:,}) rows {action}: {desc}. {Sf:,} -> {Smf:,}"


###
@register_dataframe_booster("levels")
def levels(dataframe, show_values=True):
    """
    Report the number of unique values (levels) for each variable. 
    Useful to inspect categorical variables.

    Parameters
    ----------
    show_values: bool
        Whether to report a short sample of level values.
    """
    nlvl = dataframe.nunique()
    cnt = dataframe.count().to_frame("obs")
    dtype = dataframe.dtypes.to_frame("dtype")
    levels = nlvl.to_frame("levels").join([cnt, dtype])
    levels.loc[levels.obs == 0, "obs"] = np.nan
    if show_values:
        r = []
        for li in dataframe.columns:
            unique_values = dataframe[li].unique()
            sample = ", ".join(map(str, unique_values[:5]))
            if len(unique_values) > 5:
                sample += ", ..."
            r.append(sample)
        levels["values"] = r
    levels.loc[:, "uniqueness"] = levels.levels / levels.obs
    levels = levels.sort_values("uniqueness", ascending=False)
    return levels[["levels", "obs", "dtype", "uniqueness", "values"]]


def isnotebook():
    "If code is executing in jupyter notebook"
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


@register_dataframe_booster("merge")
@wraps(pd.merge)
def check_merge(left, *args, **kwargs):
    """Merge datasets and show statistics."""
    kwargs["indicator"] = True
    right = args[0]
    mg = left.merge(*args, **kwargs)
    mgstats = mg["_merge"].value_counts()
    # report stats
    nobs_left = left.shape[0]
    nobs_right = right.shape[0]
    nobs_result = mg.shape[0]
    nobs_left_in_result = mgstats["both"] + mgstats["left_only"]
    nobs_right_in_result = mgstats["both"] + mgstats["right_only"]
    d = {
        "left": bignum(nobs_left),
        "right": bignum(nobs_right),
        "result": bignum(nobs_result),
        r"%left matched": format_percentage(nobs_left_in_result / nobs_left),
        r"%right matched": format_percentage(nobs_right_in_result / nobs_right),
    }
    rpt = pd.Series(d).to_frame().T

    if isnotebook():
        from IPython.core.display import display, HTML

        display(HTML(rpt.to_html()))
    else:
        print(rpt)
    return mg.drop("_merge", axis=1).copy()


@register_dataframe_booster("missing")
def nmissing(dataframe, show_all=False):
    """
    Evaluate the number of missing values in columns in the dataframe 
    
    Parameters
    ----------
    show_all: bool
        Whether to report all columns. `False` to show only columns with
        one or more missing values.
    """
    total = dataframe.shape[0]
    missing = pd.isnull(dataframe).sum().to_frame(name="nmissing")
    missing["pctmissing"] = (missing.nmissing / total * 100).apply(int) / 100
    missing.sort_values(by="nmissing", inplace=True)
    missing.reset_index(inplace=True)
    if not show_all:
        missing = missing.loc[missing.nmissing > 0]
    return missing
