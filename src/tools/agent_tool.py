"""
AgentTool:将SimplAgent包装为Tool，实现直接调用
相较于A2A协议更为简单易用且稳定。
"""

from hello_agents import SimpleAgent
from hello_agents.tools import Tool
from typing import Dict, Any


class AgentTool(Tool):
    """将一个SimpleAgent包装为可以直接被其他Agent调用的工具"""

    def __init__(self, agent: SimpleAgent, name: str, description: str):
        """
        param:
            agent: 要包装的SimpleAgent实例
            name: 工具名称
            description: 工具描述
        """
        self.agent = agent
        self._name = name
        self._description = description

    @property
    def name(self)->str:
        return self._name

    @property
    def description(self)->str:
        return self._description

    def get_parameters(self) -> list:
        """定义工具参数"""
        from hello_agents.tools.base import ToolParameter
        return [
            ToolParameter(
                name="query",
                type="string",
                description="发送给智能体的查询或指令",
                required=True
            )
        ]

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行工具——直接调用被包装的智能体"""
        query = parameters.get('query','')

        if not query:
            return "错误，需要提供query参数"

        try:
            return self.agent.run(query)
        except Exception as e:
            return f"调用{self.name}时出错：{str(e)}"


