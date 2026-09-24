import io
import contextlib
from hello_agents.tools import Tool
from typing import Dict,Any

class CodeRunner(Tool):
    """
    安全执行Python代码并返回输出的工具
    warning:此工具使用exec()，不适配生产环境
    """

    def __init__(self):
        super().__init__(
            name="code_runner",
            description="执行Python代码并返回标准输出/错误，输入应为包含'code'键的字典。"
        )

    def get_parameters(self)->Dict[str, str]:
        return {
            "type":"object",
            "properties":{
                "code":{
                    "type":"string",
                "description":"要执行的Python代码片段"},
            },
            "required":["code"]
        }

    def run(self,parameters:Dict[str,Any])->str:
        code = parameters.get("code","")
        if not code:
            return "错误:未提供代码。"

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                safe_globals = {
                    "__builtins__":__builtins__,
                    "print":print,
                    "range":range,
                    "len":len,
                }
                exec(code, safe_globals)

                output = stdout_capture.getvalue()
                errors = stderr_capture.getvalue()

                result = ""
                if output:
                    result += f"输出:\n{output}"
                if errors:
                    result += f"错误:\n{errors}"

                return result

        except Exception as e:
            return f"运行时错误:{str(e)}"

