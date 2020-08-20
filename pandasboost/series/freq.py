import pandas as pd
from ..datatools import bignum, format_percentage

def freq(srs, business=True, ascending=False):
    c = srs.value_counts()
    c = c.to_frame('freq')
    c['pct'] = c / c['freq'].sum()
    c = c.sort_values(by='freq', ascending=ascending)
    c['cumfreq'] = c['freq'].cumsum()
    c['cumpct'] = c['pct'].cumsum()
    if business:
        formats = {
            'freq': bignum,
            'cumfreq': bignum,
            'pct': format_percentage,
            'cumpct': format_percentage,
        }
        for col, fmt in formats.items():
            c[col] = c[col].apply(fmt)
    c = c[['freq', 'cumfreq', 'pct', 'cumpct']]
    return c


# def freq(series):
#     """Return a dataframe showing the percentage, cumulative percentage, 
#     and cumulative frequency of a series.
#     """
#     series.name='freq'
#     df = pd.DataFrame(series)
#     df['pct'] = series / series.sum()
#     df['cumfreq'] = series.cumsum()
#     df['cumpct'] = df.cumfreq / series.sum()
#     return df