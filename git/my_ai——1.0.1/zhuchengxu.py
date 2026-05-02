from shuruchuli.chulishuru import huo_qu_yong_hu_shu_ru
from renshetishi.shezhirenshe import huo_qu_ren_she
from liaotianjiyi.jiyicunchu import load_current_dai_msg, save_current_dai_msg, check_need_compress, create_new_dai, save_original_dai_msg
from moxingdiaoyong.diaoyongmoxing import get_final_reply, compress_msg_to_summary

def zhu_xun_huan():
    msg_list = load_current_dai_msg()
    ren_she = huo_qu_ren_she()

    if not msg_list:
        msg_list.append({"role":"system","content":ren_she})
        save_original_dai_msg(1, msg_list)
        save_current_dai_msg(msg_list)

    print("AI长记忆对话已启动，输入 退出 结束")

    while True:
        yong_hu_hua = huo_qu_yong_hu_shu_ru()
        if yong_hu_hua == "退出":
            print("程序已结束")
            break

        ai_hui_da = get_final_reply(msg_list, yong_hu_hua)

        msg_list.append({"role":"user","content":yong_hu_hua})
        msg_list.append({"role":"assistant","content":ai_hui_da})

        save_current_dai_msg(msg_list)

        # 现在这个方法存在、变量都导入好了，不会爆红
        if check_need_compress(msg_list):
            print(">>> 上下文超限，自动压缩生成下一代会话...")
            new_start_msg = compress_msg_to_summary(msg_list)
            create_new_dai(new_start_msg)
            msg_list = load_current_dai_msg()
            print(">>> 换代完成，开启新会话")

        print("AI：", ai_hui_da)
        print("-" * 60)

if __name__ == "__main__":
    zhu_xun_huan()