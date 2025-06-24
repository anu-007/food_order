from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from ...tools.ingredients_enrichment import ingredients_enrichment
from ...tools.callbacks.tool_callback import after_tool_logger
from ...tools.callbacks.agent_callback import before_agent_cb
from ...core.config import MODEL_TEXT
from ...prompt import dish_enrichment_prompt

ingredients_fetcher_agent = LlmAgent(
    model = LiteLlm(model=MODEL_TEXT),
    name = "info_fetcher",
    description = "Given the list of dishes fetches the ingredients, nutritional information, calories etc.",
    instruction = dish_enrichment_prompt,
    tools = [ingredients_enrichment],
    output_key = "enriched_dishes",
    before_agent_callback = before_agent_cb
)