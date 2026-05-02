AI长记忆分代对话系统 - 项目说明文档
 
1. 项目简介
 
极简版：基于大模型API的长效记忆分代对话系统，自动拆分会话代、长效留存历史语境、智能召回过往对话，自带按日模块化日志，解决上下文溢出、历史易丢失、调试无记录问题。
 
2. 核心功能
 
- 对话自动分代，超阈值自动换代封存
- 双库记忆：权重摘要库 + 关键词兜底库
- 三层检索：聚合粗筛 → 精细精筛 → 关键词兜底
- 历史片段智能萃取，节省Token保留关键语境
- 语境优先人设，会话约定高于公共常识
- 按日自动生成纯文本模块化日志
- 换代/退出自动生成摘要、关键词归档入库
 
3. 版本升级亮点
 
- 架构：普通分代升级为双库长效记忆架构
- 检索：新增三层漏斗召回，冷门历史不丢失
- 日志：重构为纯文本分块日志，按日期归档
- 稳定性：修复日志句柄冲突、导入卡死问题
- 全流程自动化：换代、归档、入库无需手动操作
 
4. 项目目录结构
 
plaintext
  
项目根目录
├── peizhi.py                # 全局配置
├── rizhicaozuo.py           # 日志处理模块
├── zhuchengxu.py            # 程序主入口
├── renshetishi/
│   └── shezhirenshe.py      # 人设提示词
├── shuruchuli/
│   └── chulishuru.py        # 用户输入处理
├── shuchuzhanshi/
│   └── chulishuchu.py       # 回复输出格式化
├── liaotianjiyi/
│   └── jiyicunchu.py        # 对话分代存档逻辑
├── moxingdiaoyong/
│   └── diaoyongmoxing.py    # 模型调用、摘要关键词萃取
├── suoyinquanzhong/
│   ├── suoyinjiegou.py      # 记忆库数据结构
│   ├── suoyincaozuo.py      # 权重索引库操作
│   ├── guanjianci caozuo.py # 关键词库操作
│   └── jiansuoliuer.py      # 检索漏斗调度
├── jiyidangan/              # 自动生成：记忆库+各代对话存档
└── rizhi/                   # 自动生成：每日模型请求日志
 
 
5. 模块功能简述
 
文件 核心作用 
peizhi.py 接口、密钥、阈值、路径全局统一配置 
rizhicaozuo.py 自动建日志目录、按日分文件、模块化写日志 
zhuchengxu.py 主循环、全流程业务调度入口 
shezhirenshe.py 定义对话语境优先级人设 
chulishuru.py 封装控制台用户输入 
chulishuchu.py 封装AI回复排版输出 
jiyicunchu.py 分代读写、长度检测、自动换代 
diaoyongmoxing.py 模型调用、摘要/关键词/历史片段萃取 
suoyinjiegou.py 规范双记忆库数据结构 
suoyincaozuo.py 索引库分区、权重更新、代归档 
guanjianci caozuo.py 关键词入库、语义兜底匹配 
jiansuoliuer.py 统一检索入口，多层级历史召回 
 
6. 运行流程
 
1. 程序启动 → 加载配置、代数、当前会话上下文
2. 用户输入 → 多层检索匹配历史对话
3. 萃取相关历史片段，拼接人设+上下文请求模型
4. 返回回答、格式化输出、写入当日日志
5. 上下文超阈值自动封存、生成新会话代
6. 输入 退出 自动归档记忆并结束程序
 
7. 部署使用
 
1. 安装依赖： pip install openai 
2. 配置 peizhi.py ：接口地址、密钥、模型名
3. 运行入口： python zhuchengxu.py 
4. 输入 退出 结束会话
5. 自动生成 jiyidangan 、 rizhi 文件夹，无需手动创建
 
8. 项目特性
 
- 模块化拆分，结构清晰易二次开发
- 长效记忆不丢失，语境连贯
- 自动控Token，避免上下文溢出
- 日志规范分块，便于调试复盘
- 全程自动化，零手动维护
 
直接全选复制，粘贴到任意Markdown编辑器/笔记文档，自动渲染标准markdown格式，简介极致精简、结构规整。
