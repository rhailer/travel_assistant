import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration with validation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your OpenAI API key:")
    print("OPENAI_API_KEY=sk-your-api-key-here")

# UI Configuration
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'accent': '#E74C3C',
    'success': '#27AE60',
    'warning': '#F39C12',
    'light': '#ECF0F1',
    'dark': '#34495E',
    'white': '#FFFFFF',
    'gray': '#95A5A6'
}

FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 16, 'bold'),
    'body': ('Segoe UI', 11),
    'small': ('Segoe UI', 9),
    'button': ('Segoe UI', 11, 'bold')
}