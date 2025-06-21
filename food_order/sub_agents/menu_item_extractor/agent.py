from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from ...tools.image_handler import process_menu_image, extract_dishes
from ...tools.callbacks.after_tool import after_tool_logger
from ...core.config import MODEL_TEXT
from ...prompt import menu_extraction_prompt

menu_item_extractor_agent = LlmAgent(
    model = LiteLlm(model=MODEL_TEXT),
    name = "menu_item_extractor",
    description = "Given the image of restaurant menu extract the dishes present in the menu",
    instruction = menu_extraction_prompt,
    tools = [process_menu_image, extract_dishes],
    output_key = "menu_dishes",
    after_tool_callback = after_tool_logger
)