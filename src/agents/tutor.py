from hello_agents import SimpleAgent,HelloAgentsLLM
from typing import Dict,Any

from hello_agents.core import llm


class TutorAgent(SimpleAgent):
    """
    主要负责协调智能体，直接管理Planner=和Exercise以及Reviewer子智能体。
    """
    def __init__(self,llm:HelloAgentsLLM):
        """
        初始化 TutorAgent 和所有子智能体。

        param:
        llm:用于所有agents的大语言模型实例。

        """
        from agents.planner import  PlannerAgent
        from agents.exercise import ExerciseAgent
        from agents.reviewer import ReviewerAgent
        from tools.code_runner import CodeRunner
        from tools.agent_tool import AgentTool

        self.planner = PlannerAgent(llm)
        self.exercise = ExerciseAgent(llm)
        self.reviewer = ReviewerAgent(llm)

        system_prompt = """
        你是一位经验丰富的智能编程导师，你负责根据用户的实际情况与需求协调智能体设计一个个性化的学习体验
        
        你拥有以下专业助手（工具）：
        -call_planner；课程规划师，负责制定个性化学习计划
        -call_exercise：出题人，负责生成编程练习题
        -call_reviewer：评审员，评审代码并提供反馈
        
        特别注意，你必须使用工具，而非自己直接完成这些任务！
        
        特别注意，工具调用格式（严格遵守此范式）
        [TOOL_CALL:工具名称:参数]
        
        具体示例：
        
        示例1 - 学习计划：
        用户："我想学习Python中的列表推导式"
        你的回答：[TOOL_CALL:call_planner:query=请为学习Python列表推导式制定学习计划]
        
        示例2 - 练习题：
        用户："请给我出一道关于列表推导式的练习题"
        你的回答：[TOOL_CALL:call_exercise:query=请出一道关于列表推导式的练习题]
        
        示例3 - 代码评审（最重要！）：
        用户："请评审以下代码: numbers = [1, 2, 3]"
        你的回答：[TOOL_CALL:call_reviewer:query=请评审以下代码: numbers = [1, 2, 3]]
        
        工作流程（必须严格遵守）：
        1. 当用户表达学习目标时 → 立即调用 call_planner
        2. 当用户请求练习时 → 立即调用 call_exercise  
        3. 当用户提交代码或请求评审时 → 立即调用 call_reviewer
        
        **绝对禁止的行为**：
        - ❌ 不要自己制定学习计划
        - ❌ 不要自己出练习题
        - ❌ 不要自己评审代码（即使代码很简单）
        - ❌ 不要说"工具调用失败"然后自己完成任务
        
        正确的行为：
        - ✅ 识别用户意图
        - ✅ 立即生成工具调用（格式：[TOOL_CALL:工具名:query=...]）
        - ✅ 等待工具返回结果
        - ✅ 将结果友好地呈现给用户
        
        """

        super().__init__(
            name="Tutor",
            llm=llm,
            system_prompt=system_prompt
        )

        # 将子智能体包装为工具并注册
        self.add_tool(AgentTool(
            self.planner,
            name="call_planner",
            description="调用课程规划师，为用户制定个性化的学习计划"
        ))

        self.add_tool(AgentTool(
            self.exercise,
            name="call_exercise",
            description="调用出题人，根据学习内容生成编程练习题"
        ))

        self.add_tool(AgentTool(
            self.reviewer,
            name="call_reviewer",
            description="调用评审员，对用户提交的代码进行评审和反馈"
        ))





