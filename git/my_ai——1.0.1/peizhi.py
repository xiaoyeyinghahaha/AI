# 大模型接口配置
# 模型全局配置
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = "b4e5748a9a4e49d988972075b2af6f92.fJfdFU3Dy0NhjYQD"
MODEL_NAME = "glm-4-flash"

# 上下文&分代规则配置
MAX_CONTEXT_CHAR = 3000       # 单代最大字符上限
COMPRESS_TRIGGER_RATE = 0.85  # 达到85%触发压缩换代
JIYI_DANGAN_WENJIANJIA = "jiyidangan"
DANGAN_DAI_CUNCHU_WENJIAN = "dai_record.txt"

# 指令标记（固定协议，给模型识别用）
NEED_HISTORY_PREFIX = "NEED_HISTORY:"


