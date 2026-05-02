from shuruchuli.chulishuru import get_user_input
from renshetishi.shezhirenshe import get_persona
from shuchuzhanshi.chulishuchu import show_answer
from liaotianjiyi.jiyicunchu import *
from moxingdiaoyong.diaoyongmoxing import *
from suoyinquanzhong.suoyincaozuo import add_dai_index, update_weight
from suoyinquanzhong.guanjiancicaozuo import add_keyword_item
from suoyinquanzhong.jiansuoliuer import search_get_dai_final

def main_loop():
    msg_list = load_current_msg()
    persona = get_persona()

    if not msg_list:
        msg_list.append({"role":"system","content":persona})
        save_original_msg(now_dai, msg_list)
        save_current_msg(msg_list)

    print("=== AI长记忆对话已启动，输入 退出 结束 ===")

    while True:
        user_q = get_user_input()
        if user_q == "退出":
            # 退出前：为本代生成摘要+关键词，写入双库
            summary = generate_topic_summary(msg_list)
            kw_str = extract_keywords_from_chat(msg_list)
            add_dai_index(now_dai, summary)
            add_keyword_item(now_dai, kw_str, summary)
            print("程序退出")
            break

        # 1. 双路径检索找相关历史代
        rel_dai = search_get_dai_final(user_q)
        append_fragment = ""

        # 2. 命中历史代：加载原文件 + 萃取片段 + 更新权重
        if rel_dai:
            history_full = load_spec_dai_original(rel_dai)
            append_fragment = extract_related_fragment(user_q, history_full)
            update_weight(rel_dai)

        # 3. 拼接上下文回答
        temp_msg = msg_list.copy()
        if append_fragment:
            temp_msg.append({"role":"assistant","content":f"历史相关上下文：{append_fragment}"})
        temp_msg.append({"role":"user","content":user_q})

        ai_ans = model_chat_once(temp_msg)
        show_answer(ai_ans)

        # 4. 存入当前会话
        msg_list.append({"role":"user","content":user_q})
        msg_list.append({"role":"assistant","content":ai_ans})
        save_current_msg(msg_list)

        # 5. 触发换代压缩
        if need_compress(msg_list):
            print(">>> 上下文超限，自动创建下一代会话...")
            summary = generate_topic_summary(msg_list)
            kw_str = extract_keywords_from_chat(msg_list)
            # 先归档当前代
            save_original_msg(now_dai, msg_list)
            add_dai_index(now_dai, summary)
            add_keyword_item(now_dai, kw_str, summary)
            # 新建空会话
            new_ctx = [{"role":"system","content":persona}]
            create_new_dai(new_ctx)
            msg_list = load_current_msg()
            print(">>> 换代完成，开启新会话")

if __name__ == "__main__":
    main_loop()