# 简单智能导师 (easy Agents tutor)

基于多智能体协作 (Multi-Agent) 与 ReAct 循环机制构建的编程学习辅助系统。系统能够根据用户目标自动制定学习计划、生成练习题，并对用户提交的代码进行沙箱执行与专业评审。

## 🎯 项目简介
随着大语言模型的发展，单一的对话式 AI 难以满足复杂的编程教学需求。本项目基于 `hello-agents` 框架，设计并实现了一个协调者-子智能体（Coordinator-Subagent）架构的编程导师系统。用户只需输入自然语言目标，系统即可自动调度不同专长的 Agent 完成任务闭环。

## ✨ 核心功能
- **个性化学习计划**：根据用户基础与目标，自动拆解里程碑并生成结构化学习路径。
- **自动出题**：针对具体知识点生成编程练习题。
- **安全代码评审**：内置 `CodeRunner` 沙箱工具，支持捕获代码的 `stdout/stderr`，评审员能结合真实的运行错误（如 `IndentationError`）给出反馈，而非单纯靠 LLM 幻觉猜测。
- **多智能体协作**：Tutor (协调者) 负责调度 Planner (规划师)、Exercise (出题人) 和 Reviewer (评审员)。

## 🏗️ 系统架构
```text
👤 用户输入
   ↓
[ Tutor Agent ] (基于 ReAct 循环的协调者)
   ↓ 意图识别，输出 [TOOL_CALL:...]
   ├─→ call_planner → PlannerAgent (制定学习计划)
   ├─→ call_exercise → ExerciseAgent (生成练习题)
   └─→ call_reviewer → ReviewerAgent (代码评审)
                          ↓
                   [ CodeRunner 工具 ] (exec 执行代码，捕获输出)


## 🚀 快速开始
1. 配置环境
bash

# 克隆项目
git clone https://github.com/你的用户名/easyAgentstutor.git
cd easyAgentstutor

# 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# 安装依赖
pip install "hello-agents[all]"
pip install python-dotenv

## 2. 配置 API Key

复制 .env.example 为 .env，填入你的 DeepSeek API Key：
env

LLM_MODEL_ID=deepseek-flash
LLM_API_KEY=sk-你的DeepSeek密钥
LLM_BASE_URL=https://api.deepseek.com

## 3. 运行项目
bash

python main.py

在终端输入你的目标（如 我想学习 Python 列表推导式 或 评测以下代码：print("hello")），系统将自动调度。
