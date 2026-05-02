from shuruchuli.chulishuru import huo_qu_yong_hu_shu_ru
from renshetishi.shezhirenshe import huo_qu_ren_she
from liaotianjiyi.jiyicunchu import jia_zai_ji_yi, jia_ru_ji_yi, huo_qu_quan_bu_ji_yi
from moxingdiaoyong.diaoyongmoxing import fa_song_wen_ti
from shuchuzhanshi.chulishuchu import xian_shi_hui_da

def zhu_xun_huan():
    # 启动先加载本地json记忆
    jia_zai_ji_yi()

    # 加载人设并加入记忆第一条
    ren_she_nei_rong = huo_qu_ren_she()
    jia_ru_ji_yi("system", ren_she_nei_rong)

    print("AI聊天程序已启动，输入 退出 关闭程序")
    while True:
        yong_hu_hua = huo_qu_yong_hu_shu_ru()

        if yong_hu_hua == "退出":
            print("程序已结束")
            break

        # 保存用户对话
        jia_ru_ji_yi("user", yong_hu_hua)

        # 调用模型
        quan_bu_ji_yi = huo_qu_quan_bu_ji_yi()
        ai_hui_da = fa_song_wen_ti(quan_bu_ji_yi)

        # 保存AI回复
        jia_ru_ji_yi("assistant", ai_hui_da)

        # 展示回答
        xian_shi_hui_da(ai_hui_da)

if __name__ == "__main__":
    zhu_xun_huan()