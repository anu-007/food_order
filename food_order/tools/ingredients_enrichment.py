from google.adk.tools import ToolContext
from litellm import completion
from ..core.config import MODEL_TEXT
from ..prompt import dish_enrichment_prompt

async def ingredients_enrichment(tool_context: ToolContext) -> dict:
    """Fetch the ingredients of each dish given a list of dishes
    
    Args:
        tool_context (ToolContext): The context object containing state
        
    Returns:
        dict: A dictionary containing status and details of each dish
    """
    try:
        print("===== Dish details enrichment ========")

        enriched_data = completion(
            model=MODEL_TEXT,
            messages=[
                {
                    "role": "user",
                    "content": dish_enrichment_prompt
                }
            ]
        )
        print('enriched_data', enriched_data)

        return {
            "status": "success",
            "data": enriched_data.choices[0].message.content
        }
    except Exception as e:
        print(f"Error enriching dish data: {e}")
        return {"status": "error", "message": str(e)}