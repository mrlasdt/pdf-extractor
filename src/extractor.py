# %%
from config.extractor import extractor as extractor_cfg
from src.prefix_extractor import PrefixExtractor, PrefixConfig
from src.table_extractor import TableExtractor, TableConfig
import pandas as pd
from pdfplumber.page import Page
import pdfplumber
from pathlib import Path
class Extractor:
    def __init__(self, cfg: dict = extractor_cfg, table_settings_path:str = "config/table_settings.yml") -> None:
        self.table_extractor = TableExtractor(table_settings_path=table_settings_path)
        self.prefix_extractor = PrefixExtractor()
        self.cfg = cfg

    def load_pdf(self, pdf_path:str) -> Page:
        pdf = pdfplumber.open(pdf_path)
        return pdf.pages[0]  # in this example, only extract the first page
    def __call__(self, pdf_path: str) -> pd.DataFrame:
        ddata = dict()
        p = self.load_pdf(pdf_path)
        for key, cfg in self.cfg.items():
            if isinstance(cfg, PrefixConfig): 
                ddata[key] = self.prefix_extractor.extract_value_from_prefix(cfg, p) 
            elif isinstance(cfg,TableConfig):
                ddata[key] = self.table_extractor.extract_value_from_table(cfg, p)
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
    