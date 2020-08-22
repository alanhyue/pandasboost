from .register import register_dataframe_booster

from .apply_mask import check_drop, check_keep

register_dataframe_booster('keep')(check_keep)
register_dataframe_booster('drop')(check_drop)