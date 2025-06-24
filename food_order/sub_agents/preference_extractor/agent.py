from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from ...tools.callbacks.agent_callback import before_agent_cb, after_agent_cb
from ...core.config import MODEL_TEXT
from ...prompt import preference_extraction_prompt

preference_extractor_agent = LlmAgent(
    model = LiteLlm(model=MODEL_TEXT),
    name = "preference_extractor",
    description = "Given the user input extract user dietery preferences",
    instruction = preference_extraction_prompt,
    output_key = "user_preferences",
    before_agent_callback = before_agent_cb,
    after_agent_callback = after_agent_cb
)