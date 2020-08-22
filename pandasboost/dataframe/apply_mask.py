def check_keep(frame, mask):
    Sf = frame.shape[0]
    Sm = mask.sum()
    mf = frame.loc[mask].copy()
    Smf = mf.shape[0]
    msg = make_msg(Sf, Sm, Smf, 'kept', mask.name)
    print(msg)
    return mf

def check_drop(frame, mask):
    Sf = frame.shape[0]
    Sm = mask.sum()
    mf = frame.loc[~mask].copy()
    Smf = mf.shape[0]
    msg = make_msg(Sf, Sm, Smf, 'dropped', mask.name)
    print(msg)
    return mf

def make_msg(Sf, Sm, Smf, action, desc):
    mPf = Sm / Sf
    return f'{mPf:.0%} ({Smf}) rows {action}: {desc}. {Sf:,} -> {Smf:,}'