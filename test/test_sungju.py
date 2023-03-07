# %%
import sys
sys.path.append("/mnt/ssd500/hungbnt/Cello")
# %%
from src.table_extractor import TableExtractor
from src.prefix_extractor import PrefixExtractor
from config.sungju_cfg import sungju as cfg
import pdfplumber
# pdf_file = "/mnt/ssd500/hungbnt/Cello/data/SL/PKVB1RQ221230BRSV11295.pdf"
pdf_file = "/mnt/ssd500/hungbnt/Cello/data/SL/PKVB1RQ230124EGSV136.pdf"
pdf = pdfplumber.open(pdf_file)
p0 = pdf.pages[0]  # in this example, only extract the first page

# %%
tab_ext = TableExtractor()
item_code = tab_ext.extract_value_from_table(cfg["item_code"], p0)
print(item_code)

# %%
package = tab_ext.extract_value_from_table(cfg["package"], p0)
print(package)
# %%
qty_unit = tab_ext.extract_value_from_table(cfg["qty_unit"], p0)
print(qty_unit)
# %%
pre_ext = PrefixExtractor()
item_name = pre_ext.extract_value_from_prefix(cfg["item_name"], p0)
print(item_name)
# %%
po_no = pre_ext.extract_value_from_prefix(cfg["po_no"], p0)
print(po_no)

#%%
uld_no = pre_ext.extract_value_from_prefix(cfg["uld_no"], p0)
print(uld_no)

# %%
p0.extract_words()

# %%
