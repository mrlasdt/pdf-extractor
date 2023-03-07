from src.table_extractor import TableConfig
from src.prefix_extractor import PrefixConfig
sungju = {
    "item_code": TableConfig(
        col_id=1,
        top_prefix=("UNIT", 'bottom'),
        bottom_prefix=("TOTAL", 'top'),
    ),
    "item_name": PrefixConfig(
        after_prefix="UNIT",
        after_offset=3,
        n_words=2,
    ),
    "po_no": PrefixConfig(
        before_prefix="CO.,LTD",
        before_offset=0,
        n_words=1,
    ),

    "uld_no": PrefixConfig(
        is_regex=True,
        after_prefix=r"ML-VN\d+",
        after_offset=1,
        n_words=1,
    ),
    "package": TableConfig(
        col_id=5,  # IF PACKAGE present in the table -> take package, else take carton
        top_prefix=("UNIT", 'bottom'),
        bottom_prefix=("TOTAL", 'top'),
    ),
    "qty_qty": TableConfig(
        col_id=3,
        top_prefix=("UNIT", 'bottom'),
        bottom_prefix=("TOTAL", 'top'),
    ),
    "qty_unit": TableConfig(
        col_id=4,
        top_prefix=("UNIT", 'bottom'),
        bottom_prefix=("TOTAL", 'top'),
    ),
}
