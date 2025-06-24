import asyncio
import io
from PIL import Image
from pathlib import Path
from typing import Optional
from food_order.runner import get_runner
from food_order.services.sessions import get_session, CustomSessionService
from food_order.services.artifacts import get_artifacts
from google.genai import types
from food_order.core.config import APP_NAME, SESSION_ID, USER_ID

async def run_conversation(menu_image_path: Path, preference_text: Optional[str] = None):
    try:
        print("\n=== Starting Food Order Workflow ===")
        
        # get session
        session = await get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        # get artifact
        artifact = get_artifacts()
        
        # get runner
        runner = get_runner(APP_NAME, session, artifact)

        # forma initial message
        img = Image.open(menu_image_path)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        image_bytes = img_byte_arr.getvalue()
        content = types.Content(role='user', parts=[types.Part(text=preference_text), types.Part.from_bytes(data=image_bytes, mime_type='image/png')])

        # run convertation
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.actions and (event.actions.escalate or event.actions.transfer_to_agent):
                await CustomSessionService.filter_events(session, APP_NAME, USER_ID, SESSION_ID)
            
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
        
        print("Workflow completed with result:", final_response_text)
        return final_response_text
        
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
