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
            
            🏨 LUXURY HOTELS (3-5 options with approximate prices per night)
            🍽️ FINE DINING (Michelin-starred restaurants with price ranges)
            ✨ EXCLUSIVE EXPERIENCES (VIP tours, private access with costs)
            🛍️ LUXURY SHOPPING (high-end boutiques, designer stores)
            🚗 PREMIUM TRANSPORTATION (luxury car services, private transfers)
            🌤️ WEATHER & PACKING ADVICE for the season
            💡 INSIDER TIPS (local secrets, best times to visit)
            
            Make it detailed and specific with actual names, addresses where possible, and realistic prices.
            Focus on ultra-luxury experiences for high-end travelers.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert luxury travel advisor with extensive knowledge of high-end destinations, 5-star hotels, Michelin restaurants, and exclusive experiences worldwide."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
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
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #2c3e50;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #3498db;
            margin: 1rem 0;
        }
        .stButton > button {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #2980b9;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="main-title">✈️ Luxury Travel Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Luxury Travel Recommendations</p>', unsafe_allow_html=True)
    
    # Check API key
    try:
        if 'OPENAI_API_KEY' not in st.secrets:
            st.error("🔑 Please add your OpenAI API key to Streamlit secrets!")
            st.info("Go to App Settings → Secrets and add: OPENAI_API_KEY = 'your-key-here'")
            return
        else:
            st.success("✅ API key configured")
    except:
        st.error("❌ Could not access Streamlit secrets")
        return
    
    # Initialize assistant
    assistant = SimpleTravelAssistant()
    
    # Get current date for date inputs
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    week_later = today + timedelta(days=7)
    
    # Input form
    with st.form("travel_form"):
        st.markdown("### 📍 Plan Your Luxury Journey")
        
        # Destination input
        destination = st.text_input(
            "🏖️ Destination", 
            placeholder="e.g., Paris, Tokyo, Maldives, Swiss Alps...",
            help="Enter your dream luxury destination"
        )
        
        # Date inputs in columns
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "📅 Start Date", 
                value=tomorrow,
                min_value=today,
                help="When does your luxury journey begin?"
            )
        
        with col2:
            # Ensure end_date is always after start_date
            min_end_date = start_date + timedelta(days=1) if start_date else tomorrow
            default_end_date = max(min_end_date, week_later)
            
            end_date = st.date_input(
                "📅 End Date", 
                value=default_end_date,
                min_value=min_end_date,
                help="When does your luxury journey end?"
            )
        
        # Submit button
        submitted = st.form_submit_button("🎯 Generate Luxury Recommendations", type="primary")
    
    # Generate recommendations
    if submitted:
        if not destination.strip():
            st.error("Please enter a destination!")
        elif start_date >= end_date:
            st.error("End date must be after start date!")
        else:
            # Calculate trip duration
            duration = (end_date - start_date).days
            
            with st.spinner(f"🔄 Curating luxury recommendations for your {duration}-day journey to {destination}..."):
                recommendations = assistant.generate_recommendations(
                    destination.strip(), 
                    start_date.strftime("%Y-%m-%d"), 
                    end_date.strftime("%Y-%m-%d")
                )
                
                st.success("✅ Your luxury recommendations are ready!")
                
                # Display results
                st.markdown("---")
                
                # Header for results
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"## 🏖️ {destination}")
                    st.markdown(f"**📅 {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}**")
                    st.markdown(f"**⏰ {duration} days of luxury**")
                
                st.markdown("---")
                
                # Show recommendations
                with st.container():
                    st.markdown(recommendations)
                
                # Add a "Plan Another Trip" button
                st.markdown("---")
                if st.button("🌟 Plan Another Luxury Trip"):
                    st.rerun()
    
    # Info section when no form is submitted
    else:
        st.markdown("---")
        
        # Feature highlights
        st.markdown("### ✨ Your Luxury Travel Experience Includes:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>🏨 Ultra-Luxury Stays</h4>
            <ul>
            <li>5-star hotels & resorts</li>
            <li>Boutique luxury properties</li>
            <li>Private villas & suites</li>
            <li>Exclusive member clubs</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
            <h4>🍽️ World-Class Dining</h4>
            <ul>
            <li>Michelin-starred restaurants</li>
            <li>Celebrity chef experiences</li>
            <li>Private dining experiences</li>
            <li>Wine & culinary tours</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
            <h4>✨ Exclusive Experiences</h4>
            <ul>
            <li>VIP tours & skip-the-line access</li>
            <li>Private guides & concierge</li>
            <li>Luxury transportation</li>
            <li>Insider local experiences</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional info
        st.markdown("---")
        st.markdown("""
        ### 🎯 How It Works:
        1. **Enter your dream destination** - anywhere in the world
        2. **Select your travel dates** - we'll consider seasonal factors
        3. **Get personalized luxury recommendations** - tailored to high-end travelers
        4. **Enjoy your perfect luxury getaway** - with insider tips and exclusive access
        """)
        
        st.markdown("""
        ### 💡 Pro Tips:
        - Our AI considers seasonal factors, local events, and weather
        - All recommendations focus on luxury and premium experiences
        - Prices are estimates - actual costs may vary
        - Book luxury experiences well in advance for best availability
        """)

if __name__ == "__main__":
    main()