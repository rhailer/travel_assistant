import streamlit as st
import requests
import json
from datetime import datetime, timedelta

class SimpleTravelAssistant:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        # Get API key from Streamlit secrets
        try:
            if 'OPENAI_API_KEY' in st.secrets:
                self.api_key = st.secrets["OPENAI_API_KEY"]
            else:
                st.error("❌ API key not found in secrets")
        except Exception as e:
            st.error(f"❌ Error accessing secrets: {e}")
    
    def generate_recommendations(self, destination, start_date, end_date):
        if not self.api_key:
            return "❌ OpenAI API key not configured. Please check your Streamlit secrets."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        You are an elite luxury travel advisor with expertise in ultra-high-end destinations worldwide. 
        
        Create comprehensive luxury travel recommendations for {destination} from {start_date} to {end_date}.
        
        Please provide detailed information in these categories:
        
        🏨 **LUXURY ACCOMMODATIONS** (3-5 options)
        - Ultra-luxury hotels, resorts, and boutique properties
        - Approximate nightly rates in USD
        - Unique features and why they're special
        - Booking recommendations
        
        🍽️ **FINE DINING EXPERIENCES** (5-7 restaurants)
        - Michelin-starred establishments
        - Celebrity chef restaurants
        - Unique culinary experiences
        - Price ranges per person
        - Reservation tips
        
        ✨ **EXCLUSIVE EXPERIENCES** (5-8 activities)
        - VIP tours and private access
        - Luxury wellness and spa treatments
        - Private cultural experiences
        - Adventure activities (luxury level)
        - Approximate costs
        
        🛍️ **LUXURY SHOPPING**
        - High-end boutiques and designer stores
        - Local luxury markets
        - Exclusive shopping districts
        - Personal shopping services
        
        🚗 **PREMIUM TRANSPORTATION**
        - Luxury car services
        - Private transfers
        - Helicopter/private jet options
        - Chauffeur services
        
        🌤️ **WEATHER & PACKING**
        - Expected weather conditions
        - What to pack for luxury activities
        - Seasonal considerations
        
        💎 **INSIDER SECRETS**
        - Hidden luxury gems only locals know
        - Best times to visit popular attractions
        - VIP access tips
        - Cultural etiquette for luxury travelers
        
        Format the response with clear headings, specific venue names, realistic prices, and actionable advice.
        Make it comprehensive yet easy to read.
        """
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are the world's leading luxury travel advisor, with exclusive access to the finest hotels, restaurants, and experiences globally. You specialize in ultra-high-end travel for discerning clients with substantial budgets."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 3000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            return content
            
        except requests.exceptions.Timeout:
            return "❌ Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"❌ Error connecting to OpenAI API: {str(e)}"
        except KeyError:
            return "❌ Unexpected response format from OpenAI API."
        except Exception as e:
            return f"❌ Error generating recommendations: {str(e)}"

def main():
    # Page config
    st.set_page_config(
        page_title="Luxury Travel Assistant",
        page_icon="✈️",
        layout="wide"
    )
    
    # Custom CSS
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
        .trip-info {
            background: linear-gradient(90deg, #3498db, #2980b9);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
            font-size: 1.1rem;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="main-title">✈️ Luxury Travel Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Ultra-Luxury Travel Recommendations</p>', unsafe_allow_html=True)
    
    # Initialize assistant
    assistant = SimpleTravelAssistant()
    
    # Only proceed if API key is configured
    if not assistant.api_key:
        st.error("🔑 Please configure your OpenAI API key in Streamlit Cloud:")
        st.markdown("""
        1. Go to your app dashboard on Streamlit Cloud
        2. Click on "Settings" → "Secrets"
        3. Add: `OPENAI_API_KEY = "your-api-key-here"`
        4. Save and restart the app
        """)
        return
    else:
        st.success("✅ API key configured")
    
    # Get current date
    today = datetime.now().date()
    
    # Input form
    with st.form("travel_form"):
        st.markdown("### 📍 Plan Your Luxury Journey")
        
        # Destination input
        destination = st.text_input(
            "🏖️ Destination", 
            placeholder="e.g., Paris, Tokyo, Maldives, Swiss Alps, Dubai...",
            help="Enter your dream luxury destination"
        )
        
        # Date inputs - FIXED VERSION
        st.markdown("#### 📅 Travel Dates")
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Start Date", 
                value=today + timedelta(days=1),  # Default to tomorrow
                min_value=today,
                help="When does your luxury journey begin?"
            )
        
        with col2:
            # Calculate suggested end date (7 days after start date)
            if start_date:
                suggested_end = start_date + timedelta(days=7)
                min_end = start_date + timedelta(days=1)
            else:
                suggested_end = today + timedelta(days=8)
                min_end = today + timedelta(days=2)
            
            end_date = st.date_input(
                "End Date", 
                value=suggested_end,
                min_value=min_end,
                help="When does your luxury journey end?"
            )
        
        # Show trip duration
        if start_date and end_date and end_date > start_date:
            duration = (end_date - start_date).days
            st.markdown(f"""
            <div class="trip-info">
            ✈️ {duration}-day luxury journey from {start_date.strftime('%B %d')} to {end_date.strftime('%B %d, %Y')}
            </div>
            """, unsafe_allow_html=True)
        elif start_date and end_date and end_date <= start_date:
            st.warning("⚠️ Please select an end date after your start date")
        
        # Submit button
        submitted = st.form_submit_button("🎯 Generate Luxury Recommendations", type="primary")
    
    # Generate recommendations
    if submitted:
        if not destination.strip():
            st.error("Please enter a destination!")
        elif not start_date or not end_date:
            st.error("Please select both start and end dates!")
        elif start_date >= end_date:
            st.error("End date must be after start date!")
        else:
            duration = (end_date - start_date).days
            
            with st.spinner(f"🔄 Curating exclusive luxury recommendations for your {duration}-day journey to {destination}..."):
                recommendations = assistant.generate_recommendations(
                    destination.strip(), 
                    start_date.strftime("%Y-%m-%d"), 
                    end_date.strftime("%Y-%m-%d")
                )
                
                # Display results
                st.markdown("---")
                
                # Header
                st.markdown(f"## 🏖️ {destination}")
                st.markdown(f"**📅 {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}**")
                st.markdown(f"**⏰ {duration} days of luxury**")
                
                st.markdown("---")
                
                # Show recommendations
                st.markdown(recommendations)
                
                # Success message
                st.success("✅ Your luxury recommendations are ready!")
                
                # Option to generate new recommendations
                if st.button("🌟 Plan Another Luxury Trip"):
                    st.rerun()
    
    # Info section when no form submitted
    else:
        st.markdown("---")
        st.markdown("### ✨ What Makes This Special:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🏨 Ultra-Luxury Stays**
            - 5-star hotels & exclusive resorts
            - Private villas & boutique properties
            - Member-only clubs & hideaways
            - Personalized service & amenities
            """)
        
        with col2:
            st.markdown("""
            **🍽️ World-Class Dining**
            - Michelin-starred restaurants  
            - Celebrity chef experiences
            - Private dining & wine tastings
            - Exclusive culinary adventures
            """)
        
        with col3:
            st.markdown("""
            **✨ Exclusive Access**
            - VIP tours & skip-the-line privileges
            - Private guides & concierge service
            - Luxury transportation & transfers
            - Insider experiences & hidden gems
            """)

if __name__ == "__main__":
    main()