# 思维实验室 🧠📈

心理学 × 经济学 × 创业思维，给大学生看的入门学习站。

不是教科书，是"能用在生活里、能拿去创业"的概念卡片。每个概念都配了**生活例子**和**创业例子**，看完就能用。

## 里面有什么

| 模块 | 内容 |
|------|------|
| 心理学 | 沉没成本、锚定效应、达克效应、损失厌恶、习得性无助…… |
| 经济学 | 机会成本、复利效应、比较优势、囚徒困境、公地悲剧…… |
| 思维模型 | 双系统思维、第一性原理、逆向思维、二阶思维 |
| 创业框架 | 精益创业、护城河、PMF、飞轮效应 |
| 创业顺序学 | 来自《创业可以学》：客户拒绝学、GTM切入、财务仪表盘…… |
| 每日一词 | 每天一个概念 + 公式 |
| 推荐书单 | 21 本，可勾选记录阅读进度（localStorage 自动保存） |

## 每日自动更新

每天 9:45（UTC 1:45），GitHub Actions 自动跑一次更新脚本：

1. 从 `scripts/concepts.json`（52 个备选概念池）挑 1-2 个没加过的概念
2. 按现有卡片格式插进页面（工作日优先经济学，周末优先心理学）
3. 更新统计数字 → commit → 部署 GitHub Pages

全程在 GitHub 服务器上跑，**不需要电脑开机**。

## 访问

🌐 **https://fishjoyness.github.io/thinking-lab/** —— GitHub Pages，每天自动更新，手机直接打开

## 技术栈

- 纯 HTML + CSS + JavaScript，零依赖，单文件
- `scripts/update_concepts.py` —— Python 更新脚本
- `scripts/concepts.json` —— 概念数据池
- `.github/workflows/daily-update.yml` —— 每日更新 + 部署（双 job）
- `.github/workflows/deploy-pages.yml` —— 手动 push 时自动部署

## 本地运行

```bash
# 更新一次概念（往 index.html 加新卡片）
python scripts/update_concepts.py
```

直接双击 `index.html` 就能在浏览器里看。
