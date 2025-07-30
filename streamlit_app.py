import streamlit as st
import os
from datetime import datetime, timedelta
import time

# Simple travel assistant without complex state management
class SimpleTravelAssistant:
    def __init__(self):
        self.client = None
        self.api_key = None
        
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
                st.error(f"Failed to initialize OpenAI: {e}")
    
    def generate_recommendations(self, destination, start_date, end_date):
        if not self.client:
            return "❌ OpenAI client not initialized. Please check your API key."
        
        try:
            prompt = f"""
            You are a luxury travel advisor. Provide detailed luxury travel recommendations for {destination} 
            from {start_date} to {end_date}. Include:
            
            1. Luxury Hotels (with approximate prices)
            2. Fine Dining Restaurants (Michelin starred preferred)
            3. Exclusive Experiences
            4. High-end Shopping
            5. Premium Transportation
            6. Weather Information
            7. Insider Tips
            
            Format as a well-structured, detailed response.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a luxury travel advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating recommendations: {str(e)}"

def main():
    # Page config
    st.set_page_config(
        page_title="Luxury Travel Assistant",
        page_icon="✈️",
        layout="wide"
    )
    
    # Title
    st.title("✈️ Luxury Travel Assistant")
    st.markdown("*AI-Powered Luxury Travel Recommendations*")
    
    # Check API key
    try:
        if 'OPENAI_API_KEY' not in st.secrets:
            st.error("🔑 Please add your OpenAI API key to Streamlit secrets!")
            st.info("Go to App Settings → Secrets and add: OPENAI_API_KEY = 'your-key-here'")
            return
        else:
            st.success("✅ API key found")
    except:
        st.error("❌ Could not access Streamlit secrets")
        return
    
    # Initialize assistant
    assistant = SimpleTravelAssistant()
    
    # Input form
    with st.form("travel_form"):
        st.subheader("📍 Plan Your Journey")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            destination = st.text_input("Destination", placeholder="e.g., Paris, Tokyo, Bali")
        
        with col2:
            start_date = st.date_input("Start Date", min_value=datetime.now().date())
        
        with col3:
            end_date = st.date_input("End Date", min_value=datetime.now().date() + timedelta(days=1))
        
        submitted = st.form_submit_button("🎯 Generate Recommendations", type="primary")
    
    # Generate recommendations
    if submitted:
        if not destination:
            st.error("Please enter a destination!")
        elif start_date >= end_date:
            st.error("End date must be after start date!")
        else:
            with st.spinner("🔄 Generating luxury recommendations..."):
                recommendations = assistant.generate_recommendations(
                    destination, 
                    start_date.strftime("%Y-%m-%d"), 
                    end_date.strftime("%Y-%m-%d")
                )
                
                st.success("✅ Recommendations generated!")
                
                # Display results
                st.markdown("---")
                st.subheader(f"🏖️ Luxury Recommendations for {destination}")
                st.markdown(f"**📅 Travel Dates:** {start_date} to {end_date}")
                
                # Show recommendations in an expandable section
                with st.expander("🌟 Your Personalized Recommendations", expanded=True):
                    st.markdown(recommendations)
    
    # Info section
    if not submitted:
        st.markdown("---")
        st.markdown("### ✨ What You'll Get:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🏨 Luxury Accommodations**
            - 5-star hotels and resorts
            - Boutique luxury properties
            - Price ranges and booking tips
            """)
        
        with col2:
            st.markdown("""
            **🍽️ Fine Dining**
            - Michelin-starred restaurants
            - Local culinary experiences
            - Reservation recommendations
            """)
        
        with col3:
            st.markdown("""
            **✨ Exclusive Experiences**
            - VIP tours and access
            - Private experiences
            - Seasonal highlights
            """)

if __name__ == "__main__":
    main()