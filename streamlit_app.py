import streamlit as st
import os
from datetime import datetime, timedelta
import threading
import time
from travel_assistant import TravelAssistant

# Page configuration
st.set_page_config(
    page_title="Luxury Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495E;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #ECF0F1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
        margin: 1rem 0;
    }
    .recommendation-section {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #BDC3C7;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background-color: #3498DB;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background-color: #2980B9;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    if 'travel_assistant' not in st.session_state:
        st.session_state.travel_assistant = None

def check_api_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("🔑 OpenAI API Key Required")
        st.markdown("""
        **To use this app, you need to set up your OpenAI API key:**
        
        1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
        2. In Streamlit Cloud, go to your app settings → Secrets
        3. Add: `OPENAI_API_KEY = "your-api-key-here"`
        
        For local development, create a `.env` file with your API key.
        """)
        return False
    return True

def format_recommendations_streamlit(recommendations, destination, start_date, end_date):
    """Format recommendations for Streamlit display"""
    
    # Header
    st.markdown(f"# 🏖️ Luxury Travel Recommendations")
    st.markdown(f"**📍 Destination:** {destination}")
    st.markdown(f"**📅 Travel Dates:** {start_date} to {end_date}")
    st.markdown("---")
    
    # Handle errors
    if "error" in recommendations:
        st.error(f"⚠️ {recommendations['error']}")
        if recommendations.get('destination_overview'):
            st.info("Showing available recommendations despite the error:")
    
    # Raw AI response (if available)
    if recommendations.get('raw_ai_response'):
        with st.expander("🤖 Complete AI Response", expanded=True):
            st.markdown(recommendations['raw_ai_response'])
        st.markdown("---")
    
    # Create columns for organized display
    col1, col2 = st.columns(2)
    
    with col1:
        # Destination Overview
        if recommendations.get('destination_overview'):
            st.markdown("## 🌟 Destination Overview")
            st.info(recommendations['destination_overview'])
        
        # Weather
        if recommendations.get('weather'):
            st.markdown("## 🌤️ Weather & Packing")
            st.info(recommendations['weather'])
        
        # Luxury Hotels
        if recommendations.get('luxury_hotels'):
            st.markdown("## 🏨 Luxury Accommodations")
            for i, hotel in enumerate(recommendations['luxury_hotels'], 1):
                if isinstance(hotel, dict):
                    with st.container():
                        st.markdown(f"**{i}. {hotel.get('name', 'N/A')}**")
                        st.markdown(f"💰 *Price: {hotel.get('price_range', 'Contact for rates')}*")
                        st.write(hotel.get('description', ''))
                        st.markdown("---")
                else:
                    st.write(f"{i}. {hotel}")
        
        # Fine Dining
        if recommendations.get('fine_dining'):
            st.markdown("## 🍽️ Fine Dining Experiences")
            for i, restaurant in enumerate(recommendations['fine_dining'], 1):
                if isinstance(restaurant, dict):
                    with st.container():
                        st.markdown(f"**{i}. {restaurant.get('name', 'N/A')}**")
                        st.markdown(f"🍳 *Cuisine: {restaurant.get('cuisine_type', 'N/A')}*")
                        st.markdown(f"💰 *Price: {restaurant.get('price_range', 'Contact for rates')}*")
                        st.write(restaurant.get('description', ''))
                        st.markdown("---")
                else:
                    st.write(f"{i}. {restaurant}")
    
    with col2:
        # Exclusive Experiences
        if recommendations.get('exclusive_experiences'):
            st.markdown("## ✨ Exclusive Experiences")
            for i, experience in enumerate(recommendations['exclusive_experiences'], 1):
                if isinstance(experience, dict):
                    with st.container():
                        st.markdown(f"**{i}. {experience.get('name', 'N/A')}**")
                        st.markdown(f"💰 *Price: {experience.get('price_range', 'Contact for rates')}*")
                        st.write(experience.get('description', ''))
                        st.markdown("---")
                else:
                    st.write(f"{i}. {experience}")
        
        # Luxury Shopping
        if recommendations.get('luxury_shopping'):
            st.markdown("## 🛍️ Luxury Shopping")
            for i, shopping in enumerate(recommendations['luxury_shopping'], 1):
                if isinstance(shopping, dict):
                    with st.container():
                        st.markdown(f"**{i}. {shopping.get('name', 'N/A')}**")
                        st.markdown(f"🏪 *Type: {shopping.get('type', 'N/A')}*")
                        st.write(shopping.get('description', ''))
                        st.markdown("---")
                else:
                    st.write(f"{i}. {shopping}")
        
        # Transportation
        if recommendations.get('transportation'):
            st.markdown("## 🚗 Luxury Transportation")
            for i, transport in enumerate(recommendations['transportation'], 1):
                if isinstance(transport, dict):
                    with st.container():
                        st.markdown(f"**{i}. {transport.get('type', 'N/A')}**")
                        st.write(transport.get('description', ''))
                        st.markdown("---")
                else:
                    st.write(f"{i}. {transport}")
    
    # Full width sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Seasonal Highlights
        if recommendations.get('seasonal_highlights'):
            st.markdown("## 🎭 Seasonal Highlights")
            for i, highlight in enumerate(recommendations['seasonal_highlights'], 1):
                st.write(f"{i}. {highlight}")
    
    with col2:
        # Insider Tips
        if recommendations.get('insider_tips'):
            st.markdown("## 💡 Insider Tips")
            for i, tip in enumerate(recommendations['insider_tips'], 1):
                st.write(f"{i}. {tip}")

def main():
    # Initialize session state
    initialize_session_state()
    
    # Check API key
    if not check_api_key():
        return
    
    # Initialize travel assistant
    if st.session_state.travel_assistant is None:
        st.session_state.travel_assistant = TravelAssistant()
    
    # Header
    st.markdown('<h1 class="main-header">✈️ Luxury Travel Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7F8C8D;">AI-Powered Luxury Travel Recommendations</p>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.markdown("## 🗺️ Plan Your Journey")
        
        # Destination input
        destination = st.text_input(
            "🏖️ Destination",
            placeholder="e.g., Paris, Tokyo, Bali...",
            help="Enter your dream destination"
        )
        
        # Date inputs
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "📅 Start Date",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )
        
        with col2:
            end_date = st.date_input(
                "📅 End Date",
                min_value=datetime.now().date() + timedelta(days=1),
                value=datetime.now().date() + timedelta(days=7)
            )
        
        # Validation
        if start_date >= end_date:
            st.error("End date must be after start date!")
            return
        
        # Generate button
        if st.button("🎯 Generate Luxury Recommendations", type="primary"):
            if not destination.strip():
                st.error("Please enter a destination!")
            else:
                st.session_state.loading = True
                st.rerun()
        
        # Info box
        st.markdown("""
        <div class="info-box">
        <strong>✨ What you'll get:</strong>
        <ul>
        <li>🏨 Luxury hotel recommendations</li>
        <li>🍽️ Michelin-starred restaurants</li>
        <li>🎭 Exclusive experiences</li>
        <li>🛍️ High-end shopping spots</li>
        <li>🚗 Premium transportation</li>
        <li>💡 Insider tips</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.loading:
        # Show loading state
        with st.spinner("🔄 Generating your luxury travel recommendations... This may take a moment."):
            try:
                # Generate recommendations
                recommendations = st.session_state.travel_assistant.generate_recommendations(
                    destination.strip(),
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d")
                )
                
                st.session_state.recommendations = recommendations
                st.session_state.destination = destination
                st.session_state.start_date = start_date
                st.session_state.end_date = end_date
                st.session_state.loading = False
                
                st.success("✅ Recommendations generated successfully!")
                time.sleep(1)  # Brief pause for user feedback
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating recommendations: {str(e)}")
                st.session_state.loading = False
    
    elif st.session_state.recommendations:
        # Display recommendations
        format_recommendations_streamlit(
            st.session_state.recommendations,
            st.session_state.destination,
            st.session_state.start_date.strftime("%Y-%m-%d"),
            st.session_state.end_date.strftime("%Y-%m-%d")
        )
        
        # Clear button
        if st.button("🔄 Generate New Recommendations"):
            st.session_state.recommendations = None
            st.session_state.loading = False
            st.rerun()
    
    else:
        # Welcome message
        st.markdown("""
        <div class="recommendation-section">
        <h2>🌟 Welcome to Your Luxury Travel Assistant</h2>
        <p>Plan your perfect luxury getaway with AI-powered recommendations tailored to your destination and travel dates.</p>
        
        <h3>🎯 What makes this special:</h3>
        <ul>
        <li><strong>Seasonal Intelligence:</strong> Recommendations adapt to the season of your travel</li>
        <li><strong>Luxury Focus:</strong> Only the finest hotels, restaurants, and experiences</li>
        <li><strong>Personalized:</strong> Tailored to your specific destination and dates</li>
        <li><strong>Comprehensive:</strong> Everything from accommodation to insider tips</li>
        </ul>
        
        <p><strong>👈 Get started by entering your destination and dates in the sidebar!</strong></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()