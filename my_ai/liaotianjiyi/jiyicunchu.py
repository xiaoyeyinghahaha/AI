import os
import json
from peizhi import *

now_dai = 1
current_msg_list = []

def init_jiyi_folder():
    if not os.path.exists(JIYI_DANGAN_WENJIANJIA):
        os.mkdir(JIYI_DANGAN_WENJIANJIA)

def get_dai_record_path():
    return os.path.join(JIYI_DANGAN_WENJIANJIA, DANGAN_DAI_CUNCHU_WENJIAN)

def save_dai_record(dai):
    with open(get_dai_record_path(), "w", encoding="utf-8") as f:
        f.write(str(dai))

def load_dai_record():
    global now_dai
    path = get_dai_record_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            now_dai = int(f.read().strip())
    return now_dai

def get_dai_file_path(dai, is_original=True):
    typ = "yuanshi" if is_original else "yasuo"
    return os.path.join(JIYI_DANGAN_WENJIANJIA, f"dai{dai}_{typ}.json")

def load_current_msg():
    global current_msg_list, now_dai
    init_jiyi_folder()
    load_dai_record()
    path = get_dai_file_path(now_dai, is_original=False)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            current_msg_list = json.load(f)
    return current_msg_list

def save_current_msg(msg_list):
    global current_msg_list
    current_msg_list = msg_list
    path = get_dai_file_path(now_dai, is_original=False)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(msg_list, f, ensure_ascii=False, indent=2)

def save_original_msg(dai, msg_list):
    path = get_dai_file_path(dai, is_original=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(msg_list, f, ensure_ascii=False, indent=2)

def load_spec_dai_original(dai):
    path = get_dai_file_path(dai, is_original=True)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def count_msg_len(msg_list):
    total = 0
    for m in msg_list:
        total += len(m.get("content",""))
    return total

def need_compress(msg_list):
    limit = MAX_CONTEXT_CHAR * COMPRESS_TRIGGER_RATE
    return count_msg_len(msg_list) >= limit

def create_new_dai(msg_list):
    global now_dai, current_msg_list
    now_dai += 1
    save_dai_record(now_dai)
    save_current_msg(msg_list)
    current_msg_list = msg_list
    return now_dai