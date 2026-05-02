# 大模型接口配置
# 模型全局配置
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
API_KEY = "b4e5748a9a4e49d988972075b2af6f92.fJfdFU3Dy0NhjYQD"
MODEL_NAME = "glm-4-flash"

# 对话分代压缩配置
MAX_CONTEXT_CHAR = 30000
COMPRESS_TRIGGER_RATE = 0.85

# 档案文件夹
JIYI_DANGAN_WENJIANJIA = "jiyidangan"
DANGAN_DAI_CUNCHU_WENJIAN = "dai_record.txt"

# 双全局库路径
SUOYIN_INDEX_PATH = "jiyidangan/lishisuoyin.json"
KEYWORD_MAP_PATH = "jiyidangan/guanjianciyingshe.json"

# 摘要索引分区配置
JINXI_QU_MAX = 20        # 精细区保留最大代数
JUHE_BAG_DAI_COUNT = 20  # 每多少代合成一个聚合包
JUHE_BAG_MAX_NUM = 5      # 聚合区最大包数，超了移入封存区

# 权重配置
WEIGHT_INIT = 1.0
WEIGHT_ADD_ON_CALL = 0.5
WEIGHT_LOW_THRESHOLD = 0.2

# 检索配置
NEED_HISTORY_PREFIX = "NEED_HISTORY:"
KEYWORD_MATCH_SCORE = 0.6  # 关键词匹配相似度阈值

