'''
A collection of data science utilities.
Most of the class and functions are Pandas related.
'''
from __future__ import print_function

from .pandas_api import register_dataframe_booster

from functools import wraps

import os
import sys, math
import numpy as np
import pandas as pd
import sqlite3


@register_dataframe_booster('merge')
@wraps(pd.merge)
def check_merge(left, *args, **kwargs):
    """Merge datasets and show statistics."""
    kwargs['indicator'] = True
    mg = left.merge(*args, **kwargs)
    # report stats
    stats = mg['_merge'].value_counts()
    stats.name = 'obs.'
    stats = stats.pipe(cum_freq)
    try:
        from IPython.core.display import display, HTML
        display(HTML(stats.to_html()))
    except ImportError:
        print(stats)
    return mg.drop('_merge', axis=1)

@register_dataframe_booster('update')
def check_update(master, withdf, match, columns):
    """Update columns in the master table with the updating table.
    Match records using 'match' as the key.
    """
    assert isinstance(
        columns, list), "columns must be a list, got {}.".format(columns)
    assert isinstance(
        match,   str), "match must be a string, got {}.".format(match)
    mastercols = master.columns
    withdfcols = withdf.columns
    for col in columns+[match]:
        assert col in mastercols, "Column '{}' not in master table.".format(col)
        assert col in withdfcols, "Column '{}' not in updating table.".format(col)

    # discard irrelevant columns in the updating table
    withdf = withdf[columns+[match]]
    # suffixes to distinguish master table columns from updating table columns
    sfx, sfy = suffixes = ('_x', '_y')
    mg = check_merge(master, withdf, how='outer', 
                     on=match, suffixes=suffixes)

    # update values
    for col in columns:
        mask = mg[col+sfy].notnull()
        mg.loc[mask, col+sfx] = mg.loc[mask, col+sfy]
        mg.drop(col+sfy, 1, inplace=True)
        mg.rename(columns={col+sfx: col}, inplace=True)
    return mg

@register_dataframe_booster('viewpct')
def pct(dataframe, axis=0):
    """Transform values in each cell to percentages repecting to
    the axis selected.

    Example:
    df = 
        Row1 1 2 3
        Row2 1 2 3
    >>> df.pipe(pct, 1)
    Out:
        Row1 50% 50% 50%
        Row2 50% 50% 50%
        Total 100% 100% 100%
    """
    if axis == 0:
        prepare = dataframe.pipe(sumup, 0, 1)
        prepare = prepare.div(prepare['Total'], axis=0)
    if axis == 1:
        prepare = dataframe.pipe(sumup, 1, 0)
        prepare = prepare.div(prepare.loc['Total', :], axis=1)
    prepare = prepare.applymap(lambda x: "{:.0%}".format(x))
    return prepare


@register_dataframe_booster('fmt')
def format_dataframe(dataframe, big=0, pct='auto'):
    """Automatically format a dataframe with business readings and percentages.
    
    Parameters
    ==========
    dataframe : pd.DataFrame
    big : int, default 0
        Precision for big numbers.
    pct : int, default 'auto'
        Precision for percentage numbers.
    """
    df = dataframe.copy()

    def is_pct(srs):
        if ('pct' in srs.name.lower()) or ('%' in srs.name) \
            or ('percent' in srs.name.lower()):
            return True
        return False
    allcols = set(df.columns)
    pctcols = {col for col in allcols if is_pct(df[col])}
    numcols = allcols - pctcols
    pctcols = list(pctcols)
    numcols = list(numcols)
    df[pctcols] = df[pctcols].applymap(lambda x: format_percentage(x, pct))
    df[numcols] = df[numcols].applymap(lambda x: bignum(x, big))
    return df

@register_dataframe_booster('markup')
def markup(dataframe, precision=0):
    """ Apply human readble formats and add total column and row """
    if isinstance(dataframe, pd.Series):
        dataframe = dataframe.to_frame()
    return dataframe.pipe(sumup, 1, 1).applymap(lambda x: bignum(x, precision))

@register_dataframe_booster('sumup')
def sumup(dataframe, row=True, column=False):
    """ Add a total row and/or a total column"""
    if row:
        rowtot = dataframe.sum(0).T
        if isinstance(dataframe.index, pd.core.index.MultiIndex):
            row_idx_lvls = len(dataframe.index.levels)
            tot_row_name = [''] * row_idx_lvls
            tot_row_name[0] = 'Total'
            rowtot.name = tuple(tot_row_name)
        else:
            rowtot.name = 'Total'
        dataframe = dataframe.append(rowtot, ignore_index=False, sort=True)
        # dataframe = pd.concat([dataframe, rowtot], axis=0, sort=False)
    if column:
        coltot = dataframe.sum(1)
        coltot.name = 'Total'
        dataframe['Total'] = coltot
        # dataframe = pd.concat([dataframe, coltot], axis=1, sort=False)
    return dataframe

@register_dataframe_booster('nmissing')
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
