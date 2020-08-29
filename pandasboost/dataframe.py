from .registration import register_dataframe_booster
import pandas as pd
from functools import wraps


### Check / Drop rows
@register_dataframe_booster("keep")
def check_keep(frame, mask):
    Sf = frame.shape[0]
    Sm = mask.sum()
    mf = frame.loc[mask].copy()
    Smf = mf.shape[0]
    msg = make_msg(Sf, Sm, Smf, "kept", mask.name)
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
    return f"{mPf:.0%} ({Smf}) rows {action}: {desc}. {Sf:,} -> {Smf:,}"


###
@register_dataframe_booster("levels")
def levels(dataframe, show_values=True):
    """Report the number of unique values (levels) for each variable. 
    Useful to inspect categorical variables.
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


@register_dataframe_booster("merge")
@wraps(pd.merge)
def check_merge(left, *args, **kwargs):
    """Merge datasets and show statistics."""
    kwargs["indicator"] = True
    mg = left.merge(*args, **kwargs)
    # report stats
    stats = mg["_merge"].value_counts()
    stats.name = "obs."
    stats = stats.pipe(cum_freq)
    try:
        from IPython.core.display import display, HTML

        display(HTML(stats.to_html()))
    except ImportError:
        print(stats)
    return mg.drop("_merge", axis=1)

@register_dataframe_booster('missing')
def nmissing(dataframe, show_all=False):
    """ Evaluate the number of missing values in columns in the dataframe """
    total = dataframe.shape[0]
    missing = pd.isnull(dataframe).sum().to_frame(name='nmissing')
    missing['pctmissing'] = (missing.nmissing / total * 100).apply(int) / 100
    missing.sort_values(by='nmissing', inplace=True)
    missing.reset_index(inplace=True)
    if not show_all:
        missing = missing.loc[missing.nmissing > 0]
    return missing
