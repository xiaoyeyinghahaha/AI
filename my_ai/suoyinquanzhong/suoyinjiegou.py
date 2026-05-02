from dataclasses import dataclass, asdict
from typing import List

# 单代精细摘要条目
@dataclass
class DaiIndex:
    dai_num: int
    summary: str
    weight: float
    create_time: str

# 聚合包条目
@dataclass
class JuheBag:
    start_dai: int
    end_dai: int
    bag_summary: str
    avg_weight: float

# 全局权重摘要索引结构
@dataclass
class GlobalIndex:
    jinxi_area: List[DaiIndex]
    juhe_area: List[JuheBag]
    fengcun_area: List[JuheBag]

# 关键词映射单条
@dataclass
class KeywordItem:
    dai_num: int
    keywords: List[str]
    topic_tag: str

# 全局关键词库结构
@dataclass
class KeywordLib:
    data: List[KeywordItem]