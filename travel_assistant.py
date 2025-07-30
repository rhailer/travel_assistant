import os
import streamlit as st

class TravelAssistant:
    def __init__(self):
        self.client = None
        
        # Get API key from Streamlit secrets
        try:
            if 'OPENAI_API_KEY' in st.secrets:
                self.api_key = st.secrets["OPENAI_API_KEY"]
            else:
                self.api_key = os.getenv("OPENAI_API_KEY")
        except:
            self.api_key = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"OpenAI initialization error: {e}")
    
    def generate_recommendations(self, destination, start_date, end_date):
        if not self.client:
            return "API client not initialized. Please check your OpenAI API key."
        
        try:
            prompt = f"""
            As a luxury travel advisor, provide comprehensive recommendations for {destination} 
            from {start_date} to {end_date}. Include:
            
            🏨 LUXURY HOTELS (3-5 options with prices)
            🍽️ FINE DINING (Michelin-starred restaurants)
            ✨ EXCLUSIVE EXPERIENCES (VIP tours, private access)
            🛍️ LUXURY SHOPPING (high-end boutiques, markets)
            🚗 PREMIUM TRANSPORTATION (luxury car services, private transfers)
            🌤️ WEATHER & PACKING ADVICE
            💡 INSIDER TIPS (local secrets, best times to visit attractions)
            
            Make it detailed and specific with actual names and approximate prices.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert luxury travel advisor with extensive knowledge of high-end destinations worldwide."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"