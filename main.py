import asyncio
from pathlib import Path
from typing import Optional
from food_order.runner import get_runner
from food_order.services.sessions import get_session
from food_order.services.artifacts import get_artifacts
from google.genai import types
from google.adk.runners import Runner
from food_order.core.config import APP_NAME, SESSION_ID, USER_ID
from food_order.prompt import workflow_instruction

async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    try:
        final_response_text = "Agent did not produce a final response."
        content = types.Content(role='user', parts=[types.Part(text=query)])

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break
            print(f"======Event text:===== {event.content.parts[0].text}")
        
        print("Workflow completed with result:", final_response_text)
        return final_response_text
    except Exception as e:
        print(f"Error in call_agent_async: {e}")
        raise

async def run_conversation(menu_image_path: Path, preference_text: Optional[str] = None):
    try:
        print("\n=== Starting Food Order Workflow ===")
        print(f"Menu image path: {menu_image_path}")
        print(f"User preferences: {preference_text}")
        
        session = get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        artifact = get_artifacts()
        
        runner = get_runner(APP_NAME, session, artifact)
        initial_message = preference_text
        await call_agent_async(initial_message, runner=runner, user_id=USER_ID, session_id=SESSION_ID)
        
    except Exception as e:
        print(f"Error in run_conversation: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        PROJECT_ROOT = Path(__file__).parent
        MENU_PATH = PROJECT_ROOT / "data" / "rest_1_menu.png"

        if not MENU_PATH.exists():
            raise FileNotFoundError(f"Menu image not found at: {MENU_PATH}")

        preference_text = """I'm allergic to dairy and nuts. I prefer vegetarian food, and I love Italian and Mexican cuisines. I can handle medium spicy food."""
        
        asyncio.run(run_conversation(MENU_PATH, preference_text))
    except Exception as e:
        print(f"Application error: {e}")
        exit(1)
