import os
from datetime import datetime
import json

class TravelAssistant:
    def __init__(self):
        self.client = None
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("⚠️  OpenAI API key not found!")
            return
            
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            print("✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def get_season(self, date_str):
        """Determine season based on date"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            month = date_obj.month
            
            if month in [12, 1, 2]:
                return "winter"
            elif month in [3, 4, 5]:
                return "spring"
            elif month in [6, 7, 8]:
                return "summer"
            else:
                return "autumn"
        except:
            return "spring"
    
    def generate_recommendations(self, destination, start_date, end_date):
        """Generate travel recommendations using OpenAI"""
        
        # Check if client is initialized
        if not self.client:
            return {
                "error": "OpenAI client not initialized. Please check your API key.",
                "destination_overview": f"Unable to connect to OpenAI API for {destination} recommendations.",
                "weather": "Please check local weather forecasts manually.",
                "luxury_hotels": [
                    {
                        "name": "API Connection Error",
                        "price_range": "N/A",
                        "description": "Please verify your OpenAI API key is correct and has sufficient credits."
                    }
                ],
                "fine_dining": [],
                "exclusive_experiences": [],
                "luxury_shopping": [],
                "transportation": [],
                "seasonal_highlights": ["Check your .env file for OPENAI_API_KEY"],
                "insider_tips": ["Ensure your API key starts with 'sk-' and is valid"]
            }
        
        season = self.get_season(start_date)
        
        # Calculate trip duration
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            duration = (end - start).days
        except:
            duration = 7
        
        prompt = f"""
        You are a luxury travel advisor specializing in high-end experiences. Generate detailed recommendations for a luxury traveler visiting {destination} from {start_date} to {end_date} ({season} season, {duration} days).

        Please provide recommendations in the following JSON format:
        {{
            "destination_overview": "Brief overview of the destination during this season",
            "weather": "Expected weather conditions and what to pack",
            "luxury_hotels": [
                {{
                    "name": "Hotel Name",
                    "price_range": "Price per night",
                    "description": "Why this hotel is perfect for luxury travelers"
                }}
            ],
            "fine_dining": [
                {{
                    "name": "Restaurant Name",
                    "cuisine_type": "Type of cuisine",
                    "price_range": "Price per person",
                    "description": "What makes this restaurant special"
                }}
            ],
            "exclusive_experiences": [
                {{
                    "name": "Experience Name",
                    "price_range": "Estimated cost",
                    "description": "Detailed description of the exclusive experience"
                }}
            ],
            "luxury_shopping": [
                {{
                    "name": "Shopping Location",
                    "type": "Type of shopping (boutiques, markets, etc.)",
                    "description": "What luxury items or experiences are available"
                }}
            ],
            "transportation": [
                {{
                    "type": "Transportation Type",
                    "description": "Luxury transportation options and costs"
                }}
            ],
            "seasonal_highlights": [
                "Special events, festivals, or seasonal attractions during this time"
            ],
            "insider_tips": [
                "Exclusive tips that only luxury travel advisors would know"
            ]
        }}

        Focus on:
        - Ultra-luxury accommodations (5-star hotels, luxury resorts)
        - Michelin-starred restaurants and exclusive dining experiences
        - Private tours, VIP access, and unique experiences
        - High-end shopping and exclusive boutiques
        - Premium transportation options
        - Seasonal considerations and weather-appropriate activities
        - Insider knowledge for luxury travelers

        Provide specific names, realistic price ranges, and detailed descriptions. Respond ONLY with valid JSON.
        """
        
        try:
            print(f"🔄 Generating recommendations for {destination}...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using 3.5-turbo as it's more stable and cost-effective
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a world-class luxury travel advisor. Always respond with valid JSON only."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            print("✅ Received response from OpenAI")
            
            # Try to extract and parse JSON
            try:
                # Remove any markdown formatting
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                # Find JSON boundaries
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    recommendations = json.loads(json_str)
                    print("✅ Successfully parsed JSON response")
                    return recommendations
                else:
                    raise json.JSONDecodeError("No JSON found", content, 0)
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON parsing failed: {e}")
                return self._create_fallback_response(content, destination, season)
                
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return {
                "error": f"API Error: {str(e)}",
                "destination_overview": f"Failed to generate recommendations for {destination}. Error: {str(e)}",
                "weather": "Please check local weather forecasts.",
                "luxury_hotels": [
                    {
                        "name": "Service Temporarily Unavailable",
                        "price_range": "N/A",
                        "description": "Please try again in a moment."
                    }
                ],
                "fine_dining": [],
                "exclusive_experiences": [],
                "luxury_shopping": [],
                "transportation": [],
                "seasonal_highlights": ["Please try again later"],
                "insider_tips": ["Check your internet connection and API credits"]
            }
    
    def _create_fallback_response(self, content, destination, season):
        """Create a fallback response when JSON parsing fails"""
        return {
            "destination_overview": f"AI recommendations for {destination} in {season}",
            "weather": f"Check local weather for {destination} during {season}",
            "luxury_hotels": [
                {
                    "name": "AI Generated Content",
                    "price_range": "See details below",
                    "description": "Full AI response provided in raw format below."
                }
            ],
            "fine_dining": [
                {
                    "name": "See AI Response",
                    "cuisine_type": "Various",
                    "price_range": "Luxury",
                    "description": "Detailed recommendations in the raw AI response."
                }
            ],
            "exclusive_experiences": [
                {
                    "name": "Custom Recommendations",
                    "price_range": "Premium",
                    "description": "See full AI response for detailed experiences."
                }
            ],
            "luxury_shopping": [
                {
                    "name": "Premium Shopping",
                    "type": "Various",
                    "description": "Shopping recommendations in full response."
                }
            ],
            "transportation": [
                {
                    "type": "Luxury Options",
                    "description": "Transportation details in AI response."
                }
            ],
            "seasonal_highlights": [f"Seasonal information for {season} in {destination}"],
            "insider_tips": ["Full AI response contains detailed insider knowledge"],
            "raw_ai_response": content
        }