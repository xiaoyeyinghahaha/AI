import json
import os
from peizhi import *
from dataclasses import dataclass, asdict
from suoyinquanzhong.suoyinjiegou import KeywordLib, KeywordItem

def init_keyword_lib():
    if not os.path.exists(JIYI_DANGAN_WENJIANJIA):
        os.mkdir(JIYI_DANGAN_WENJIANJIA)
    if not os.path.exists(KEYWORD_MAP_PATH):
        empty = KeywordLib(data=[])
        with open(KEYWORD_MAP_PATH, "w", encoding="utf-8") as f:
            json.dump(asdict(empty), f, ensure_ascii=False, indent=2)

def load_keyword_lib() -> KeywordLib:
    init_keyword_lib()
    with open(KEYWORD_MAP_PATH, "r", encoding="utf-8") as f:
        return KeywordLib(**json.load(f))

def save_keyword_lib(lib: KeywordLib):
    with open(KEYWORD_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(lib), f, ensure_ascii=False, indent=2)

def add_keyword_item(dai_num: int, keyword_str: str, topic_tag: str):
    """新增一代关键词记录，永久保存不删除"""
    lib = load_keyword_lib()
    kw_list = [k.strip() for k in keyword_str.split(",") if k.strip()]
    item = KeywordItem(
        dai_num=dai_num,
        keywords=kw_list,
        topic_tag=topic_tag
    )
    lib.data.append(item)
    save_keyword_lib(lib)

def match_keyword_get_dai(user_question: str) -> int | None:
    """关键词模糊匹配兜底，返回匹配的代编号"""
    lib = load_keyword_lib()
    q_words = set(user_question.split())
    best_dai = None
    best_score = 0
    for item in lib.data:
        hit = len(set(item.keywords) & q_words)
        score = hit / (len(item.keywords)+1)
        if score > KEYWORD_MATCH_SCORE and score > best_score:
            best_score = score
            best_dai = item.dai_num
    return best_dai