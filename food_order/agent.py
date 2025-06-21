from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .sub_agents.menu_item_extractor.agent import menu_item_extractor_agent
from .sub_agents.ingredients_fetcher.agent import ingredients_fetcher_agent
from .sub_agents.preference_extractor.agent import preference_extractor_agent
from .core.config import MODEL_TEXT
from .prompt import dish_ordering_instruction
from .tools.store_state import store_to_state
from .tools.callbacks.after_tool import after_tool_logger

# root agent
root_agent = LlmAgent(
    name = "dish_ordering_agent",
    model = LiteLlm(model=MODEL_TEXT),
    description = "Given a restaurnat menu and optional preference extract ingredients and suggest dishes to order",
    instruction = dish_ordering_instruction,
    tools = [
        store_to_state
    ],
    sub_agents = [
        preference_extractor_agent,
        menu_item_extractor_agent,
        ingredients_fetcher_agent
    ],
    output_key = 'suggested_dishes',
    after_tool_callback = after_tool_logger
)