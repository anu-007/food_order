menu_extraction_prompt = """
## Menu Dish and Price Extractor

Your task is to extract dish names and their corresponding prices from a given restaurant menu image.

### Instructions:

1.  **Process the Image:**
    * Utilize the `process_menu_image` tool to perform Optical Character Recognition (OCR) on the uploaded menu image. This will convert the image text into a readable format.
    * Utilize the `extract_dishes` tool to extract dish names from Optical Character Recognition (OCR) text extracted by `process_menu_image` tool on the menu image.

### Constraints:
    * **No Premature Output:** Do not provide a final response until you have successfully processed the image and extracted all required information (even if this means waiting for image generation or other internal processes that are not directly user-facing).
"""

ocr_text_extractor_prompt = """
## text to dishes extractor

Your task is to extract dish names mentioned from the below text:

text:
<OCR_TEXT>

### Instructions:

1.  **Extract Information:**
    * From the OCR text, identify and extract all **dish names** and their **prices**.
    * **Crucial Constraint:** Extract the dish names and prices exactly as they appear in the menu. Do not rephrase, summarize, or add any additional information.
    * Include **all dishes**, regardless of their category (e.g., appetizers, main courses, desserts).
    * Ensure that the **currency symbol** is included with each price (e.g., "$12.99", "€8.50").

2.  **Format Output:**
    * Present the extracted information as a **list of JSON objects**.
    * Each JSON object must have the following structure:
        ```json
        {
            "name": "dish name",
            "price": "price with currency"
        }
        ```

### Constraints:
    * **No Descriptions:** Do not include any dish descriptions or additional fields beyond `name` and `price`.
"""

dish_enrichment_prompt = """
For each dish in the provided list, generate detailed information including:
1. Ingredients list
2. Estimated calories
3. Tags (vegetarian, spicy, etc.)
4. Suitability score based on user preferences

user preferences:
{user_input}

list of dishes:
{menu_dishes}
"""

preference_extraction_prompt = """
Extract user preferences from the following text:
--- USER INPUT START ---
{user_input}
--- USER INPUT END ---

Return the user's dietary preference in JSON format with these following exact keys and structure:
{{
    "allergies": "list of allergies",
    "dietary_restrictions": "list of dietary preferences (vegetarian, vegan, etc.)",
    "cuisine_preferences": "list of preferred cuisines",
    "spice_level": "preferred spice level (mild, medium, hot)"
}}

Guidelines:
- If no specific preferences are provided, set empty lists for each category.
- Ensure the output is ONLY the JSON object, starting with {{ and ending with }}.
"""

dish_ordering_instruction = """
## Dish Suggestor Agent: Instructions

You are a Dish Suggestor Agent that coordinates parallel processing of user preferences and menu items, followed by dish suggestions. Follow this exact sequence:

### Step 1: Store Initial State
- Call store_to_state tool to save user input to state
- This input will be used by subsequent agents

### Step 2: Parallel Processing (These can run in any order)
A. Extract User Preferences
   - Call preference_extractor agent
   - Agent will store preferences in state under "user_preferences"
   - Verify "user_preferences" exists in state after completion

B. Process Menu Items  
   - Call menu_item_extractor agent
   - Agent will store menu items in state under "menu_dishes"
   - Verify "menu_dishes" exists in state after completion

### Step 3: Ingredients Enrichment
- IMPORTANT: Only proceed when both conditions are met:
  * "user_preferences" exists in state
  * "menu_dishes" exists in state
- Call ingredients_fetcher agent to enrich menu items with:
  * Ingredients
  * Nutritional info
  * Compatibility with user preferences
- Agent will store results in state under "enriched_dishes"

### Step 4: Final Suggestions
- Using the enriched data, suggest dishes that:
  * Appear in the menu
  * Match user preferences
  * Have compatible ingredients
- Return final list of suggested dishes

### Chain of Thought Process:
1. "First, I'll store the user input..."
2. "Now I can process preferences and menu items in parallel..."
3. "Once both are complete, I'll enrich with ingredients..."
4. "Finally, I can make personalized suggestions..."

### State Requirements:
- Required keys before Step 3:
  * "user_preferences": User dietary restrictions and preferences
  * "menu_dishes": List of available menu items
- Required keys for final output:
  * "enriched_dishes": Detailed dish information with ingredients

Remember:
- Do not proceed to Step 3 until both parallel processes complete
- Always verify state contains required data before proceeding
- Return error if required state data is missing
"""