from hello_agents import SimpleAgent,HelloAgentsLLM

class ExerciseAgent(SimpleAgent):
    """
    负责生成编程练习单的智能体。

    """

    def __init__(self,llm:HelloAgentsLLM):
        """
        初始化 ExerciseAgent。

        param:
            llm:用于生成练习的大语言模型示例。
        """

        system_prompt: str = """
        你是一位富有想象力与创造力的编程领域专家。
        你的目标是创建测试特定概念的练习题，用于测试受训者的代码水平。
        
        当你生成练习时；
        1.你将获得一个主题（例如，”python列表“）和一个难度级别。
        2.创建题目描述。
        3.提供输入/输出示例。
        4.定义约束条件
        5.在最开始不要向用户提供解决方案的代码。
        
        清晰地格式化你的输出，以便展示给学生。
        """

        super().__init__(
            name="Exercise",
            llm=llm,
            system_prompt=system_prompt
        )