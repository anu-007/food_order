import io
from litellm import completion
from google.adk.tools import ToolContext
from ..core.config import MODEL_TEXT
from ..prompt import ocr_text_extractor_prompt

import pytesseract
from PIL import Image

async def process_menu_image(tool_context: ToolContext) -> str:
    """Extract text from image.
    
    Args:
        tool_context (ToolContext): The context object containing state
        
    Returns:
        str: OCR text extracted from the image
    """
    try:
        print(" ========= Processing menu image =========")
        image_raw = tool_context.user_content.parts[1].inline_data.data
        image_bytes = io.BytesIO(image_raw)

        if not image_bytes:
            print("No image path found in context")
            return "No menu image path provided"
        
        image = Image.open(image_bytes)
        image_text = pytesseract.image_to_string(image, lang='eng')

        tool_context.state["ocr_text"] = image_text
        return image_text
    except Exception as e:
        print(f"Error processing image: {e}")
        return f"Error processing image: {str(e)}"

async def extract_dishes(tool_context: ToolContext) -> dict:
    """Extract the name of the dishes from text
    
    Args:
        tool_context (ToolContext): The context object containing state
        
    Returns:
        str: dishes names extreacted from the text
    """
    try:
        print("===== Dish name extraction ========")
        ocr_text_extractor_prompt_enriched = ocr_text_extractor_prompt.replace("<OCR_TEXT>", tool_context.state.get("ocr_text"))

        response = completion(
            model = MODEL_TEXT,
            messages=[
                {
                    "role": "user",
                    "content": ocr_text_extractor_prompt_enriched
                }
            ]
        )
        enriched_data = response.choices[0].message.content

        tool_context.state["menu_dishes"] = enriched_data
        return { "status": "success", "message": enriched_data }
    except Exception as e:
        print(f"Error enriching dish data: {e}")
        return { "status": "error", "message": str(e)}