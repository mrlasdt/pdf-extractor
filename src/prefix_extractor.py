from pdfplumber.page import Page
from typing import Optional
import re
class PrefixConfig:
    #find words between before_prefix and after_prefix. if either one is not provided, n_words is use to extract the specific number of words before or after a prefix
    def __init__(self, before_prefix:str='', before_offset:int = 0, after_prefix:str='', after_offset:int= 0, n_words:int=0, is_regex:bool= False):
        self.is_regex = is_regex
        self.before_prefix = before_prefix
        self.before_offset = before_offset #number of words in between the prefix and the item
        self.after_prefix = after_prefix
        self.after_offset=after_offset 
        self.n_words=n_words 

class PrefixExtractor:
    def __init__(self) -> None:
        super(PrefixExtractor, self).__init__()

    @staticmethod
    def find_value_after_a_prefix(lwords:list[str], prefix:str, offset:int, n_words:int, is_regex:bool)->list[str]:
        for i, word in enumerate(lwords):
            is_match = word["text"] == prefix if not is_regex else re.match(prefix, word["text"])
            if is_match:
                return [w["text"] for w in lwords[i+1+offset:i+1+offset+n_words]]
        return [""]
    @staticmethod
    def words2str(words:list[str])->str:
        return " ".join(words).strip()

    def extract_value_from_prefix(self, cfg:PrefixConfig, p:Page) -> str:
        lwords = p.extract_words()
        lwords_reverse = lwords[::-1]
        if cfg.before_prefix and cfg.after_prefix:
            words_bf = self.find_value_after_a_prefix(lwords_reverse, cfg.after_prefix, cfg.after_offset, cfg.n_words, cfg.is_regex)
            words_af = self.find_value_after_a_prefix(lwords, cfg.before_prefix, cfg.before_offset, cfg.n_words,cfg.is_regex)
            if not words_bf == words_af:
                raise ValueError("Cannot find value by prefix, check your config")
            return self.words2str(words_af)
        elif cfg.after_prefix:
            words_bf = self.find_value_after_a_prefix(lwords_reverse, cfg.after_prefix, cfg.after_offset, cfg.n_words, cfg.is_regex)
            return self.words2str(words_bf[::-1])
        elif cfg.before_prefix:
            words_af = self.find_value_after_a_prefix(lwords, cfg.before_prefix, cfg.before_offset, cfg.n_words, cfg.is_regex)
            return self.words2str(words_af)
        else:
            raise ValueError("Either before_prefix and after_prefix must be provided")
    