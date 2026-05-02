import json
import os
import time
from dataclasses import dataclass, asdict
from typing import List
from peizhi import *
from suoyinquanzhong.suoyinjiegou import GlobalIndex, DaiIndex, JuheBag

def init_index_file():
    if not os.path.exists(JIYI_DANGAN_WENJIANJIA):
        os.mkdir(JIYI_DANGAN_WENJIANJIA)
    if not os.path.exists(SUOYIN_INDEX_PATH):
        empty = GlobalIndex(jinxi_area=[], juhe_area=[], fengcun_area=[])
        with open(SUOYIN_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(asdict(empty), f, ensure_ascii=False, indent=2)

def load_global_index() -> GlobalIndex:
    init_index_file()
    with open(SUOYIN_INDEX_PATH, "r", encoding="utf-8") as f:
        return GlobalIndex(**json.load(f))

def save_global_index(idx: GlobalIndex):
    with open(SUOYIN_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(idx), f, ensure_ascii=False, indent=2)

def add_dai_index(dai_num: int, summary: str):
    """新增一代精细摘要索引"""
    g_idx = load_global_index()
    new_item = DaiIndex(
        dai_num=dai_num,
        summary=summary,
        weight=WEIGHT_INIT,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    g_idx.jinxi_area.append(new_item)

    # 精细区超限 -> 打包聚合
    if len(g_idx.jinxi_area) > JINXI_QU_MAX:
        pack_list = g_idx.jinxi_area[:JUHE_BAG_DAI_COUNT]
        remain_list = g_idx.jinxi_area[JUHE_BAG_DAI_COUNT:]
        start = pack_list[0].dai_num
        end = pack_list[-1].dai_num
        avg_w = sum(x.weight for x in pack_list) / len(pack_list)
        bag = JuheBag(
            start_dai=start,
            end_dai=end,
            bag_summary=f"第{start}-{end}代聚合历史摘要",
            avg_weight=avg_w
        )
        g_idx.jinxi_area = remain_list
        g_idx.juhe_area.append(bag)

        # 聚合区超限 移入封存区
        if len(g_idx.juhe_area) > JUHE_BAG_MAX_NUM:
            move_bag = g_idx.juhe_area.pop(0)
            g_idx.fengcun_area.append(move_bag)
    save_global_index(g_idx)

def update_weight(dai_num: int):
    """调用后提升对应代权重"""
    g_idx = load_global_index()
    for item in g_idx.jinxi_area:
        if item.dai_num == dai_num:
            item.weight += WEIGHT_ADD_ON_CALL
            break
    save_global_index(g_idx)