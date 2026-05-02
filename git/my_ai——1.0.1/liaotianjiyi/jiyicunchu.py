import os
import json
# 导入配置常量，解决变量爆红
from peizhi import (
    JIYI_DANGAN_WENJIANJIA,
    DANGAN_DAI_CUNCHU_WENJIAN,
    MAX_CONTEXT_CHAR,
    COMPRESS_TRIGGER_RATE
)

now_dai_shu = 1
current_msg_list = []

def init_jiyi_folder():
    if not os.path.exists(JIYI_DANGAN_WENJIANJIA):
        os.mkdir(JIYI_DANGAN_WENJIANJIA)

def _get_dai_record_path():
    return os.path.join(JIYI_DANGAN_WENJIANJIA, DANGAN_DAI_CUNCHU_WENJIAN)

def save_dai_record(dai_shu):
    with open(_get_dai_record_path(), "w", encoding="utf-8") as f:
        f.write(str(dai_shu))

def load_dai_record():
    global now_dai_shu
    path = _get_dai_record_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            now_dai_shu = int(f.read().strip())
    return now_dai_shu

def get_dai_file_path(dai_shu, is_yuanshi=True):
    lei_xing = "yuanshi" if is_yuanshi else "yasuo"
    return os.path.join(JIYI_DANGAN_WENJIANJIA, f"dai{dai_shu}_{lei_xing}.json")

def load_current_dai_msg():
    global current_msg_list, now_dai_shu
    init_jiyi_folder()
    load_dai_record()
    file_path = get_dai_file_path(now_dai_shu, is_yuanshi=False)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            current_msg_list = json.load(f)
    return current_msg_list

def save_current_dai_msg(msg_list):
    global current_msg_list
    current_msg_list = msg_list
    file_path = get_dai_file_path(now_dai_shu, is_yuanshi=False)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(msg_list, f, ensure_ascii=False, indent=2)

def save_original_dai_msg(dai_shu, msg_list):
    file_path = get_dai_file_path(dai_shu, is_yuanshi=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(msg_list, f, ensure_ascii=False, indent=2)

def load_spec_dai_msg(dai_shu):
    file_path = get_dai_file_path(dai_shu, is_yuanshi=True)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def count_msg_list_len(msg_list):
    total = 0
    for m in msg_list:
        total += len(m.get("content", ""))
    return total

# 补全你缺失爆红的这个方法
def check_need_compress(msg_list):
    total_len = count_msg_list_len(msg_list)
    trigger_len = MAX_CONTEXT_CHAR * COMPRESS_TRIGGER_RATE
    return total_len >= trigger_len

def create_new_dai(new_msg_list):
    global now_dai_shu, current_msg_list
    now_dai_shu += 1
    save_dai_record(now_dai_shu)
    save_current_dai_msg(new_msg_list)
    current_msg_list = new_msg_list
    return now_dai_shu