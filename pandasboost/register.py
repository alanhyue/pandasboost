from .dataframe.register import register_dataframe_booster

from .dataframe.apply_mask import check_drop, check_keep
from .dataframe.levels import levels

register_dataframe_booster("keep")(check_keep)
register_dataframe_booster("drop")(check_drop)
register_dataframe_booster("levels")(levels)
