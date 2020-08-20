import pandas as pd
def cut_groups(srs, rules, right=True, missing='missing'):
    sample_item = rules[0]
    if isinstance(sample_item, (int, float)):
        bins = rules
        labels = ['<={}'.format(c) for c in bins]
    elif isinstance(sample_item, tuple):
        bins = []
        labels = []
        for item in rules:
            bins.append(item[0])
            labels.append(item[1])
    _min = srs.min()
    if _min < bins[0]:
        bins = [_min,] + bins
    else:
        labels = labels[1:]
    if right:
        largest_bin_cut =  bins[-1]
        _max = srs.max()
        if _max > largest_bin_cut:
            bins.append(_max)
            if right == True:
                right_label = f'>{largest_bin_cut}'
            else:
                right_label = right
            labels.append(right_label)
    labels = ['{}. {}'.format(i+1,v) for i,v in enumerate(labels)]
    cuts = pd.cut(srs, bins=bins, labels=labels, include_lowest=True)
    if missing is not None:
        labels = cuts.astype(str)
        missing_label = '0. {}'.format(missing)
        labels = labels.replace('nan', missing_label)
    return labels
