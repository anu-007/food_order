from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Dict, Any
from typing import Optional

def after_tool_logger(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """Inspects/modifies the tool result after execution."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"\n[DEBUG] ========== After Tool Execution Info ==========")
    print(f"[DEBUG] Agent: {agent_name}")
    print(f"[DEBUG] Tool: {tool_name}")
    print(f"[DEBUG] Tool Args: {args}")
    print(f"[DEBUG] Tool Response: {tool_response}")
    
    print("[DEBUG] =======================================\n")
    return None