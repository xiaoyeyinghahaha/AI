from peizhi import *
from suoyinquanzhong.suoyincaozuo import load_global_index
from suoyinquanzhong.guanjiancicaozuo import match_keyword_get_dai
from moxingdiaoyong.diaoyongmoxing import model_chat_once

def rough_filter_juhe(user_q: str) -> int | None:
    """第一层：聚合包粗筛"""
    g_idx = load_global_index()
    if not g_idx.juhe_area:
        return None
    text = "\n".join([
        f"聚合包：第{b.start_dai}-{b.end_dai}代，概要：{b.bag_summary}"
        for b in g_idx.juhe_area
    ])
    prompt = [
        {"role":"system","content":"判断用户问题是否匹配某个聚合包，只返回包序号(0开始)，无匹配返回none"},
        {"role":"user","content":f"问题：{user_q}\n聚合包列表：\n{text}"}
    ]
    res = model_chat_once(prompt).strip()
    if res.isdigit():
        idx = int(res)
        if 0 <= idx < len(g_idx.juhe_area):
            return g_idx.juhe_area[idx].start_dai
    return None

def fine_filter_jinxi(user_q: str) -> int | None:
    """第二层：精细区单代精筛"""
    g_idx = load_global_index()
    if not g_idx.jinxi_area:
        return None
    text = "\n".join([
        f"第{d.dai_num}代：{d.summary}"
        for d in g_idx.jinxi_area
    ])
    prompt = [
        {"role":"system","content":"选出最相关的代编号，无匹配返回none"},
        {"role":"user","content":f"问题：{user_q}\n代摘要列表：\n{text}"}
    ]
    res = model_chat_once(prompt).strip()
    return int(res) if res.isdigit() else None

def search_get_dai_final(user_q: str) -> int | None:
    """双路径检索总入口：先摘要漏斗，再关键词兜底"""
    # 路径1：权重摘要检索
    dai = rough_filter_juhe(user_q)
    if not dai:
        dai = fine_filter_jinxi(user_q)
    # 路径2：关键词兜底
    if not dai:
        dai = match_keyword_get_dai(user_q)
    return dai