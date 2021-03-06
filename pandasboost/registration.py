from .pandas_flavor import register_dataframe_accessor, register_series_accessor
from functools import wraps


@register_dataframe_accessor("bs")
class DataFrameBooster:
    def __init__(self, obj):
        self._obj = obj


def register_dataframe_booster(name):
    def decorator(f):
        # hack
        @wraps(f)
        def wrapper(*args, **kwargs):
            instance = args[0]
            args = args[1:]
            return f(instance._obj, *args, **kwargs)

        setattr(DataFrameBooster, name, wrapper)
        return f

    return decorator


@register_series_accessor("bs")
class SeriesBooster:
    def __init__(self, obj):
        self._obj = obj


def register_series_booster(name):
    def decorator(f):
        # hack
        @wraps(f)
        def wrapper(*args, **kwargs):
            instance = args[0]
            args = args[1:]
            return f(instance._obj, *args, **kwargs)

        setattr(SeriesBooster, name, wrapper)
        return f

    return decorator
