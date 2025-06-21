import json
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DishImage(BaseModel):
    url: str
    alt_text: Optional[str] = None

class NutrientInfo(BaseModel):
    protein_percent: Optional[float] = Field(None, description="Protein percentage of daily value or total calories")
    carbs_percent: Optional[float] = Field(None, description="Carbohydrate percentage")
    fat_percent: Optional[float] = Field(None, description="Fat percentage")

class Dish(BaseModel):
    name: str
    description: Optional[str] = None
    images: List[DishImage] = []
    ingredients: List[str] = []
    estimated_calories: Optional[int] = None
    nutrient_info: Optional[NutrientInfo] = None
    calorie_classification: Optional[str] = Field(None, description="e.g., Low, Medium, High, Very High")
    tags: List[str] = []
    allergy_warnings: List[str] = []
    suitability_score: float = Field(1.0, description="Score based on user preferences, 1.0 is a perfect match")

class ProcessedMenu(BaseModel):
    dishes: List[Dish]
    user_preferences: Optional[List[str]] = None
    user_allergies: Optional[List[str]] = None

class RawDishInfo(BaseModel):
    name: str
    price: Optional[str] = None

class UserPreferences:
    allergies: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    cuisine_preferences: Optional[List[str]] = None
    spice_level: Optional[str] = None