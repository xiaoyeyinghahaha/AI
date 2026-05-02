import json
import os

# 记忆文件名称
jiyi_wen_jian = "jiyi.json"
# 全局记忆列表
ji_yi_lie_biao = []

# 从json加载记忆
def jia_zai_ji_yi():
    global ji_yi_lie_biao
    if os.path.exists(jiyi_wen_jian):
        with open(jiyi_wen_jian, "r", encoding="utf-8") as f:
            ji_yi_lie_biao = json.load(f)

# 保存记忆到json
def bao_cun_ji_yi():
    with open(jiyi_wen_jian, "w", encoding="utf-8") as f:
        json.dump(ji_yi_lie_biao, f, ensure_ascii=False, indent=2)

# 添加单条记忆并自动保存
def jia_ru_ji_yi(jue_se, nei_rong):
    ji_yi_lie_biao.append({"role": jue_se, "content": nei_rong})
    bao_cun_ji_yi()

# 获取全部记忆
def huo_qu_quan_bu_ji_yi():
    return ji_yi_lie_biao

# 清空记忆
def qing_kong_ji_yi():
    global ji_yi_lie_biao
    ji_yi_lie_biao = []
    bao_cun_ji_yi()