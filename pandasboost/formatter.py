def format_percentage(n, precision="auto"):
    """Display a decimal number in percentage.
    
    Parameters
    =========
    n : float
        The number to format.
    percision: int, str, default 'auto'
        The precision of outcome. Default 'auto' to automatically
        choose the least precision on which the outcome is not zero.

    Examples
    ========
    format_percentage(0.001) ==> '0.1%'
    format_percentage(-0.0000010009) ==> '-0.0001%'
    format_percentage(0.001, 4) ==> '0.1000%'
    """
    if precision == "auto":
        if n != 0:
            k = abs(n) * 100
            cnt = 0
            while k < 1:
                k = k * 10
                cnt += 1
            precision = cnt
        else:
            precision = 0
    fmt = "{:." + str(precision) + "%}"
    return fmt.format(n)


def bignum(n, precision=0):
    """ Transform a big number into a business style representation.
    
    Example:
    >>> bignum(123456)
    Output: 123K
    """
    millnames = ["", "K", "M", "B", "T"]
    try:
        n = float(n)
        millidx = max(
            0,
            min(
                len(millnames) - 1,
                int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3)),
            ),
        )
        fmt = "{:." + str(precision) + "f} {}"
        return fmt.format(n / 10 ** (3 * millidx), millnames[millidx])
    except ValueError:
        return n
