# 1. 环境设置
import os
import sys
import re
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM

load_dotenv()
if "src" not in sys.path:
    sys.path.append(os.path.abspath("src"))

from agents.tutor import TutorAgent


# ==========================================
# 2. 核心函数：封装 ReAct 循环
# ==========================================
def run_agent_loop(agent: TutorAgent, user_goal: str, max_steps: int = 5) -> str:
    """执行智能体循环，直到获得最终回复"""
    user_goal = user_goal.replace('\\n', '\n')
    current_prompt = f"用户说: '{user_goal}'. 请为用户制定学习计划。"

    for step in range(max_steps):
        response = agent.run(current_prompt)

        # 使用 findall 提取所有工具调用
        tool_matches = re.findall(r"\[TOOL_CALL:(.*?):query=(.*?)\]", response, re.DOTALL)

        # 如果没有工具调用，直接返回最终结果
        if not tool_matches:
            return response

        # 用一个列表来收集所有工具的返回结果
        all_tool_results = []

        for tool_name, query in tool_matches:
            query = query.strip()
            agent_attr_name = tool_name.replace("call_", "")

            print(f"⏳ 正在调用 [{agent_attr_name}] 为你处理...")

            target_agent = getattr(agent, agent_attr_name, None)

            if not target_agent:
                tool_result = f"错误：未找到名为 {agent_attr_name} 的子智能体"
            else:
                tool_result = target_agent.run(query)

            # 记录每个工具的调用结果
            all_tool_results.append(f"工具 {tool_name} 的执行结果是：\n{tool_result}")

        # 把所有结果合并，统一发给 LLM 进行最后润色
        combined_results = "\n\n---\n\n".join(all_tool_results)
        current_prompt = (
            f"以下是各个工具的执行结果：\n\n{combined_results}\n\n"
            f"请根据以上所有结果，给用户一个完整的、条理清晰的最终回复。"
        )

    return "流程超时，未获得最终结果。"


# ==========================================
# 3. 主程序入口
# ==========================================
if __name__ == "__main__":
    # 环境配置与初始化 LLM
    print("✅ 环境配置完成")
    llm = HelloAgentsLLM()
    print("✅ LLM 已初始化")

    print("创建智能编程导师...")
    tutor = TutorAgent(llm)
    print("\n✅ Tutor 初始化完成！ (Planner / Exercise / Reviewer 已就绪)")

    # 开启循环对话
    print("智能编程导师已上线！(输入 '退出' 或 'quit' 结束程序)")

    while True:
        print("-" * 40)
        user_goal = input("👤 你的目标: ").strip()

        if user_goal.lower() in ['退出', 'quit', 'exit', 'q']:
            print("👋 再见，祝你学习顺利！")
            break
        if not user_goal:
            print("⚠️ 输入不能为空，请重新输入。")
            continue

        #  执行循环，打印最终结果
        final_response = run_agent_loop(tutor, user_goal)

        # 最终结果统一在 main 函数中打印
        print("\n" + "=" * 20 + " 最终回复 " + "=" * 20)
        print(final_response)
        print("=" * 50)