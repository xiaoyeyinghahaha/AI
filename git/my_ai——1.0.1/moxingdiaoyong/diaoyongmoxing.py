from openai import OpenAI
from peizhi import BASE_URL, API_KEY, MODEL_NAME, NEED_HISTORY_PREFIX
from liaotianjiyi.jiyicunchu import count_msg_list_len, create_new_dai, load_spec_dai_msg

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=30
)

def chat_model_once(msg_list):
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=msg_list
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"模型调用异常：{str(e)}"

def compress_msg_to_summary(old_msg_list):
    prompt = [
        {"role":"system","content":"把下面对话精简浓缩成关键摘要，保留核心话题与重要信息。"},
        {"role":"user","content":f"对话内容：\n{str(old_msg_list)}"}
    ]
    summary = chat_model_once(prompt)
    new_msg = [
        {"role":"system","content":"你是接地气、简洁连贯的AI助手。"},
        {"role":"assistant","content":f"历史对话摘要：{summary}"}
    ]
    return new_msg

def parse_need_history(reply_text):
    if reply_text.startswith(NEED_HISTORY_PREFIX):
        try:
            dai_num = int(reply_text.replace(NEED_HISTORY_PREFIX, "").strip())
            return dai_num
        except:
            return None
    return None

def get_final_reply(current_msg_list, user_text):
    rule_prompt = [
        {"role":"system","content":"信息足够就直接正常回答；缺早期历史只返回格式：NEED_HISTORY:数字，不要多余文字。"},
        {"role":"user","content":f"用户问题：{user_text}\n当前上下文：{str(current_msg_list)}"}
    ]
    first_reply = chat_model_once(rule_prompt)
    need_dai = parse_need_history(first_reply)

    if need_dai is None:
        return first_reply

    history_msg = load_spec_dai_msg(need_dai)
    if not history_msg:
        return f"未找到第{need_dai}代历史记录，请直接回答当前问题。"

    extract_prompt = [
        {"role":"system","content":"从历史记录里筛选和当前问题相关的关键信息，精简摘要。"},
        {"role":"user","content":f"用户问题：{user_text}\n历史记录：{str(history_msg)}"}
    ]
    history_summary = chat_model_once(extract_prompt)

    final_msg = current_msg_list + [
        {"role":"assistant","content":f"补充历史信息摘要：{history_summary}"},
        {"role":"user","content":user_text}
    ]
    return chat_model_once(final_msg)