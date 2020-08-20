from .register import register_series_booster

from .cut_groups import cut_groups
from .freq import freq

register_series_booster('cut_groups')(cut_groups)
register_series_booster('freq')(freq)

