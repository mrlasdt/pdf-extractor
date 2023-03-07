# %%
from config.global_cfg import HEADERS
from config.sungju_cfg import sungju as sungju_cfg
from src.prefix_extractor import PrefixExtractor, PrefixConfig
from src.table_extractor import TableExtractor, TableConfig
import pandas as pd
from pdfplumber.page import Page
import pdfplumber
from pathlib import Path
class Extractor(PrefixExtractor, TableExtractor):
    def __init__(self, cfg: dict = sungju_cfg) -> None:
        super(Extractor, self).__init__()
        self.cfg = cfg

    def load_pdf(self, pdf_path:str) -> Page:
        pdf = pdfplumber.open(pdf_path)
        return pdf.pages[0]  # in this example, only extract the first page
    def __call__(self, pdf_path: str) -> pd.DataFrame:
        ddata = dict()
        p = self.load_pdf(pdf_path)
        for key, cfg in self.cfg.items():
            if isinstance(cfg, PrefixConfig): 
                ddata[key] = self.extract_value_from_prefix(cfg, p) 
            elif isinstance(cfg,TableConfig):
                ddata[key] = self.extract_value_from_table(cfg, p)
            else:
                raise ValueError("Invalid config")
        return pd.DataFrame.from_dict(ddata)

#%%
if __name__ == '__main__':
    #%%
    pdf_files = ["data/SL/PKVB1RQ221230BRSV11295.pdf", 
                 "data/SL/PKVB1RQ230124BRSV144A.pdf"]
    save_dir = "results"
    extractor = Extractor()
    for pdf_file in pdf_files:
        df = extractor(pdf_file).to_csv(Path(save_dir).joinpath(str(Path(pdf_file).stem) + ".csv"))
    