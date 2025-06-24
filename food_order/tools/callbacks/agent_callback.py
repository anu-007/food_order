from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

def before_agent_cb(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Before-Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Before-Callback] Current State: {current_state}")

    return None


def after_agent_cb(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    # session.events have all the events in chronological order
    
    

    if agent_name == 'preference_extractor':
        callback_context.state["user_preferences"] = callback_context.state.get("user_preferences") or callback_context.state.get("user_input")
        callback_context.state["preferences_complete"] = True
    print(f"\n[After-Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[After-Callback] Current State: {current_state}")

    return None