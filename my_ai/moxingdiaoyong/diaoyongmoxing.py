from openai import OpenAI
from peizhi import BASE_URL, API_KEY, MODEL_NAME
# 导入日志写入函数
from rizhicaozuo import xie_moxing_qingqiu_rizhi

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=30
)


def model_chat_once(messages):
    """单次调用大模型 + 记录完整请求日志到文件"""
    try:
        # 写入本次完整请求上下文到日志文件
        xie_moxing_qingqiu_rizhi(messages)

        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        err_msg = f"模型调用异常：{str(e)}"
        # 异常也写入日志
        xie_moxing_qingqiu_rizhi({"error": err_msg, "req_messages": messages})
        return err_msg


def generate_topic_summary(chat_history):
    prompt = [
        {"role": "system", "content": "请精简总结这段对话的核心主题，控制在50字以内。"},
        {"role": "user", "content": str(chat_history)}
    ]
    return model_chat_once(prompt)


def extract_keywords_from_chat(chat_history):
    prompt = [
        {"role": "system", "content": "提取这段对话的核心关键词、专有名词、话题名词，用逗号分隔，不要多余解释。"},
        {"role": "user", "content": str(chat_history)}
    ]
    return model_chat_once(prompt)


def extract_related_fragment(question, full_history):
    prompt = [
        {"role": "system",
         "content": "从下面完整历史对话中，只截取和用户当前问题强相关的内容，精简保留关键上下文，无关内容全部删掉。"},
        {"role": "user", "content": f"用户问题：{question}\n完整历史：{str(full_history)}"}
    ]
    return model_chat_once(prompt)