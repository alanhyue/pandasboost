
def levels(dataframe, show_values=True):
    """Report the number of unique values (levels) for each variable. 
    Useful to inspect categorical variables.
    """
    nlvl = dataframe.nunique()
    cnt = dataframe.count().to_frame('obs')
    dtype = dataframe.dtypes.to_frame('dtype')
    levels = nlvl.to_frame('levels').join([cnt, dtype])
    levels.loc[levels.obs==0, 'obs'] = np.nan
    if show_values:
        r = []
        for li in dataframe.columns:
            unique_values = dataframe[li].unique()
            sample = ', '.join(map(str, unique_values[:5]))
            if len(unique_values) > 5:
                sample += ', ...'
            r.append(sample)
        levels['values'] = r
    levels.loc[:, 'uniqueness'] = (levels.levels / levels.obs)
    levels = levels.sort_values('uniqueness', ascending=False)
    return levels[['levels', 'obs', 'dtype', 'uniqueness', 'values']]

