# 海上风电行业信息采集 Agent

自动采集、筛选、分析海上风电行业动态，生成结构化报告并发送至邮箱。

## 架构

```
offshore_wind_agent/
├── main.py                  # 主流程编排
├── scheduler.py             # 定时任务
├── sources/
│   ├── sources_config.py    # 信息源配置（RSS / 爬虫 / Google News）
│   ├── rss_collector.py     # RSS 采集
│   └── web_scraper.py       # 网页爬取 + Google News 搜索
├── storage/
│   └── database.py          # SQLite 存储（去重 + 历史记录）
├── processing/
│   └── analyzer.py          # Claude LLM 筛选与分析
├── output/
│   ├── report_generator.py  # HTML / Markdown 报告生成
│   └── email_sender.py      # 邮件发送（SMTP）
├── data/                    # SQLite 数据库（自动创建）
├── reports/                 # 生成的报告（自动创建）
├── requirements.txt
└── .env.example
```

## 信息源分类

| 类别 | 来源 | 采集方式 |
|------|------|----------|
| 行业组织 | GWEC、WindEurope、ACP | RSS |
| 政府监管 | BOEM、Crown Estate、DESNZ | 爬虫 |
| 行业媒体 | Recharge News、Windpower Monthly、Offshore Wind Biz、4C Offshore | RSS |
| 国内媒体 | 北极星风力发电网、风能专委会 | RSS |
| 主要公司 | Orsted、Vestas、Siemens Gamesa | RSS |
| 聚合搜索 | Google News 关键词搜索 | RSS API |

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 ANTHROPIC_API_KEY、SMTP_* 等

# 3. 测试运行（不调用 LLM，不发邮件）
python main.py --dry-run

# 4. 正式运行
python main.py

# 5. 定时运行（每周一 08:00 UTC）
python scheduler.py --schedule weekly
```

## 流程说明

```
采集(RSS+爬虫+GoogleNews)
    ↓
去重(SQLite URL 唯一索引)
    ↓
LLM快速打分(claude-haiku，1-5分)
    ↓
过滤低价值项(< 3分丢弃)
    ↓
LLM深度分析(claude-sonnet)
    → 中文标题 / 核心内容 / 影响分析 / 标签 / 价值评分
    ↓
生成 HTML + Markdown 报告
    ↓
SMTP 发送至 1873149332@qq.com
```

## 筛选标准

LLM 按以下维度判断信息价值：
- **政策**：补贴政策、招标制度、审批变化
- **项目进展**：中标、FID、开工、并网
- **业绩/订单**：主要公司财务、订单披露
- **行业数据**：装机量、招标量、价格指数
- **市场情绪**：融资、并购、破产事件

## 环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 密钥（必填） |
| `SMTP_HOST` | SMTP 服务器（默认 smtp.qq.com） |
| `SMTP_PORT` | SMTP 端口（默认 465） |
| `SMTP_USER` | 发件邮箱 |
| `SMTP_PASS` | 邮箱授权码（不是登录密码） |
| `REPORT_RECIPIENT` | 收件邮箱（默认 1873149332@qq.com） |

## QQ 邮箱授权码获取

1. 登录 QQ 邮箱 → 设置 → 账户
2. 开启 SMTP 服务
3. 获取授权码（16位）填入 `SMTP_PASS`
