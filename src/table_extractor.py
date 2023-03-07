from pdfplumber.page import Page
import pandas as pd
from collections import defaultdict
from typing import Optional
import yaml


class TableConfig:
    
    def __init__(
            self, tab_id: int = 0, col_id: int = 0, col_l2r: bool = True, top_prefix: tuple[str, str] = ("", ""),
            bottom_prefix: tuple[str, str] = ("", ""),
            top_offset: Optional[int] = None, bottom_offset: Optional[int] = None):
        self.tab_id = tab_id
        self.col_id = col_id
        self.col_l2r = col_l2r
        self.top_prefix = top_prefix
        self.top_offset = top_offset
        self.bottom_prefix = bottom_prefix
        self.bottom_offset = bottom_offset


class TableExtractor:
    def __init__(self, table_settings_path: str) -> None:
        super(TableExtractor, self).__init__()
        with open(table_settings_path) as f:
            self.table_settings = yaml.safe_load(f)

    @staticmethod
    def find_bbox_by_prefix(cfg: TableConfig, p: Page) -> tuple[float, float, float, float]:
        lwords = p.extract_words()
        bbox = [0, -1, p.width, -1]
        for word in lwords:
            if word["text"] == cfg.top_prefix[0] and bbox[1] == -1:
                bbox[1] = word.get(cfg.top_prefix[1])
            if word["text"] == cfg.bottom_prefix[0] and bbox[3] == -1:
                bbox[3] = word.get(cfg.bottom_prefix[1])
            if bbox[1] != -1 and bbox[3] != -1:
                break  # break when we found the bounding box
        assert bbox[1] != -1, "Table not found by top prefix, check your config"
        assert bbox[3] != -1, "Table not found by bottom prefix, check your config"
        return tuple(bbox)

    @staticmethod
    def filter_short_list_in_lists(lists: list[list]) -> list[list]:
        # Find the maximum length of all lists
        max_length = len(lists[0])
        # Remove lists that do not have the maximum length
        lists = [lst for lst in lists if len(set(lst)) > int(max_length * 0.5)]
        return lists

    def extract_table_from_page(self, cfg: TableConfig, p: Page) -> pd.DataFrame:
        bbox = self.find_bbox_by_prefix(cfg, p)
        table = p.within_bbox(bbox, relative=False).extract_table(table_settings=self.table_settings)
        table = self.filter_short_list_in_lists(table)  # remove row with nan values
        table = pd.DataFrame(table[cfg.top_offset:cfg.bottom_offset])
        return table

    def extract_value_from_table(self, cfg: TableConfig, p: Page) -> list[str]:
        table = self.extract_table_from_page(cfg, p)
        value = table.iloc[:, cfg.col_id] if cfg.col_l2r else table.iloc[:, -cfg.col_id]
        return value.to_list()
