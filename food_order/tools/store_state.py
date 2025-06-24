from google.genai import types
from google.adk.tools import ToolContext

async def store_to_state(tool_context: ToolContext, **args) -> dict[str, str]:
    """Stores user input to state that will be used by other tools and sub agents.

    Args:
      tool_context: ToolContext object.

    Returns:
      A dict with "status" and (optional) "error_message" keys.
    """
    print("==================== store state ==================")

    tool_context.state["user_input"] = tool_context.user_content.parts[0].text
    return {"status": "ok"}