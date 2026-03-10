from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompt_loader import report_prompt, system_prompt


@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    logger.info(f"[monitor_tool]tool execute: {request.tool_call["name"]}")
    logger.info(f"[monitor_tool]tool request: {request.tool_call["args"]}")

    try:
        result = handler(request)

        logger.info(f"[monitor_tool]{request.tool_call["name"]} executed successfully: {result}")

        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True
        return result
    except Exception as e:
        logger.error(f"[monitor_tool]{request.tool_call["name"]} execute error: {str(e)}")
        raise e


@before_model
def log_before_model(
        state: AgentState,      # 整个agent中的状态记录
        runtime: Runtime        # 整个执行中的上下文信息
):
    logger.info(f"[log_before_model]model is about to invoke, with {len(state["messages"])} messages")
    logger.debug(f"[log_before_model]{type(state["messages"][-1])} | {state["messages"][-1].content.strip()}")

    return None


@dynamic_prompt         # 每一次提示词生成之前调用此函数
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:       # 需要生成报告
        return report_prompt
    return system_prompt
