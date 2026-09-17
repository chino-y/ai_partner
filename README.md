# AI 智能伴侣 (ai_partner)

一个基于 DeepSeek 大模型的 **AI 智能伴侣聊天应用**，附带 DeepSeek API 本地调用的最小示例。

## ✨ 功能特性

- 💬 **AI 智能伴侣**：自定义昵称与性格，模拟真实伴侣语气流式对话
- 💾 **会话管理**：新建、保存、加载、删除历史会话（自动存入 `sessions/` 目录）
- 🚀 **本地调用示例**：DeepSeek API 的最简调用演示

## 📁 项目结构

```
.
├── 1.deepseek本地调用.py   # DeepSeek API 最小调用示例
├── 2.ai_patner.py          # Streamlit 版 AI 智能伴侣主程序
└── sessions/               # 会话记录（运行后自动生成，已 gitignore）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai streamlit astropy
```

> 💡 `astropy` 仅为兼容 `2.ai_patner.py` 中一行冗余 import；删除该行后可省略此依赖。

### 2. 设置 API Key

请通过环境变量传入 DeepSeek API Key，**不要硬编码到代码中**：

```powershell
$env:DEEPSEEK_API_KEY = "你的 DeepSeek API Key"
```

### 3. 运行

```bash
# 启动 AI 智能伴侣
streamlit run 2.ai_patner.py

# 或运行最小调用示例
python 1.deepseek本地调用.py
```

## 📖 使用说明

1. 打开应用后，在侧边栏「AI控制面板」点击「新建会话」
2. 在「伴侣信息」中填写昵称与性格（如：乐乐 / 可爱）
3. 在底部聊天框输入消息，即可与 AI 伴侣对话
4. 会话可随时「保存会话」，并在「会话历史」中加载或删除

## ⚠️ 注意事项

- 务必通过环境变量 `DEEPSEEK_API_KEY` 注入密钥，切勿提交到仓库
- `sessions/` 目录中的聊天记录为个人隐私，请勿公开分享
