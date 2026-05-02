from openai import OpenAI
from peizhi import BASE_URL, API_KEY, MODEL_NAME, MAX_CONTEXT_CHAR


def calc_all_context_len(jiyi_list):
    """计算整条上下文所有文字总字符数"""
    total_len = 0
    for msg in jiyi_list:
        total_len += len(msg.get("content", ""))
    return total_len


def fa_song_wen_ti(ji_yi):
    # 1. 先做上下文长度校验
    total_len = calc_all_context_len(ji_yi)
    print(f"当前上下文字符总数：{total_len}，配置上限：{MAX_CONTEXT_CHAR}")

    if total_len > MAX_CONTEXT_CHAR:
        tip = f"提示：上下文已超出配置最大长度{MAX_CONTEXT_CHAR}，请清理聊天记录或调高配置阈值"
        print(tip)
        return tip

    # 2. 没超限再调用模型
    try:
        client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
            timeout=30
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=ji_yi
        )

        if hasattr(response, "choices") and response.choices:
            return response.choices[0].message.content.strip()

        if hasattr(response, "data") and response.data:
            return response.data[0].text.strip()

        if hasattr(response, "content"):
            return response.content.strip()

        print("模型返回未知格式，原始数据：", response)
        return "模型返回格式不兼容"

    except Exception as e:
        print("调用模型出错：", str(e))
        return "接口或密钥异常"