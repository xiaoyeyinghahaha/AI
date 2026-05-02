import os
from datetime import datetime

RIZHI_FOLDER = "rizhi"

def init_rizhi_wenjianjia():
    if not os.path.exists(RIZHI_FOLDER):
        os.mkdir(RIZHI_FOLDER)

def get_rizhi_wenjian_ming():
    init_rizhi_wenjianjia()
    date_str = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(RIZHI_FOLDER, f"moxing_qingqiu_{date_str}.log")

def xie_moxing_qingqiu_rizhi(messages):
    init_rizhi_wenjianjia()
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_lines = []
    # 1. 先空一行，和上一个模块拉开距离
    log_lines.append("")
    # 2. 虚线分隔线
    log_lines.append("----------------------------------------")
    # 3. 时间戳
    log_lines.append(f"【{time_str}】")
    # 4. 本次完整上下文对话
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "").strip()
        if role == "user":
            log_lines.append(f"用户：{content}")
        elif role == "assistant":
            log_lines.append(f"模型：{content}")

    log_content = "\n".join(log_lines)
    with open(get_rizhi_wenjian_ming(), "a", encoding="utf-8") as f:
        f.write(log_content)