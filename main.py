import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import threading
from config import COLORS, FONTS
from travel_assistant import TravelAssistant

class TravelAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Luxury Travel Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['light'])
        
        # Initialize travel assistant
        self.travel_assistant = TravelAssistant()
        
        # Configure styles
        self.setup_styles()
        
        # Create main interface
        self.create_interface()
        
        # Center the window
        self.center_window()
    
    def setup_styles(self):
        """Configure custom styles for ttk widgets"""
        style = ttk.Style()
        
        # Configure button style
        style.configure('Custom.TButton',
                       font=FONTS['button'],
                       padding=(20, 10))
        
        # Configure label style
        style.configure('Title.TLabel',
                       font=FONTS['title'],
                       background=COLORS['light'],
                       foreground=COLORS['primary'])
        
        style.configure('Heading.TLabel',
                       font=FONTS['heading'],
                       background=COLORS['light'],
                       foreground=COLORS['dark'])
        
        style.configure('Body.TLabel',
                       font=FONTS['body'],
                       background=COLORS['light'],
                       foreground=COLORS['dark'])
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_interface(self):
        """Create the main interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['light'], padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Luxury Travel Assistant", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Input section
        self.create_input_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)
    
    def create_input_section(self, parent):
        """Create the input section"""
        input_frame = tk.Frame(parent, bg=COLORS['white'], relief='raised', bd=1)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Inner padding frame
        inner_frame = tk.Frame(input_frame, bg=COLORS['white'], padx=30, pady=20)
        inner_frame.pack(fill='x')
        
        # Section title
        section_title = ttk.Label(inner_frame, text="Plan Your Luxury Journey", style='Heading.TLabel')
        section_title.grid(row=0, columnspan=3, pady=(0, 20), sticky='w')
        
        # Destination
        ttk.Label(inner_frame, text="Destination:", style='Body.TLabel').grid(row=1, column=0, sticky='w', padx=(0, 10))
        self.destination_var = tk.StringVar()
        destination_entry = tk.Entry(inner_frame, textvariable=self.destination_var, 
                                   font=FONTS['body'], width=25, relief='solid', bd=1)
        destination_entry.grid(row=1, column=1, padx=(0, 20), pady=5, sticky='w')
        
        # Start date
        ttk.Label(inner_frame, text="Start Date:", style='Body.TLabel').grid(row=2, column=0, sticky='w', padx=(0, 10))
        self.start_date = DateEntry(inner_frame, width=12, background=COLORS['secondary'],
                                  foreground='white', borderwidth=1, font=FONTS['body'],
                                  mindate=datetime.now().date())
        self.start_date.grid(row=2, column=1, padx=(0, 20), pady=5, sticky='w')
        
        # End date
        ttk.Label(inner_frame, text="End Date:", style='Body.TLabel').grid(row=3, column=0, sticky='w', padx=(0, 10))
        self.end_date = DateEntry(inner_frame, width=12, background=COLORS['secondary'],
                                foreground='white', borderwidth=1, font=FONTS['body'],
                                mindate=datetime.now().date() + timedelta(days=1))
        self.end_date.grid(row=3, column=1, padx=(0, 20), pady=5, sticky='w')
        
        # Generate button
        self.generate_btn = tk.Button(inner_frame, text="Generate Recommendations",
                                    command=self.generate_recommendations,
                                    bg=COLORS['secondary'], fg=COLORS['white'],
                                    font=FONTS['button'], relief='flat',
                                    padx=30, pady=12, cursor='hand2')
        self.generate_btn.grid(row=4, columnspan=2, pady=20, sticky='w')
        
        # Loading label
        self.loading_label = ttk.Label(inner_frame, text="", style='Body.TLabel')
        self.loading_label.grid(row=5, columnspan=3, pady=5)
    
    def create_results_section(self, parent):
        """Create the results section"""
        results_frame = tk.Frame(parent, bg=COLORS['white'], relief='raised', bd=1)
        results_frame.pack(fill='both', expand=True)
        
        # Inner padding frame
        inner_frame = tk.Frame(results_frame, bg=COLORS['white'], padx=30, pady=20)
        inner_frame.pack(fill='both', expand=True)
        
        # Section title
        self.results_title = ttk.Label(inner_frame, text="Your Luxury Travel Recommendations", 
                                     style='Heading.TLabel')
        self.results_title.pack(anchor='w', pady=(0, 15))
        
        # Scrollable text area for results
        self.results_text = scrolledtext.ScrolledText(inner_frame, 
                                                    font=FONTS['body'],
                                                    wrap=tk.WORD,
                                                    relief='solid',
                                                    bd=1,
                                                    padx=15,
                                                    pady=15)
        self.results_text.pack(fill='both', expand=True)
        
        # Initial message
        self.results_text.insert('1.0', "Enter your destination and travel dates above, then click 'Generate Recommendations' to receive personalized luxury travel suggestions powered by AI.")
        self.results_text.config(state='disabled')
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.destination_var.get().strip():
            messagebox.showerror("Error", "Please enter a destination.")
            return False
        
        start = self.start_date.get_date()
        end = self.end_date.get_date()
        
        if start >= end:
            messagebox.showerror("Error", "End date must be after start date.")
            return False
        
        if start < datetime.now().date():
            messagebox.showerror("Error", "Start date cannot be in the past.")
            return False
        
        return True
    
    def generate_recommendations(self):
        """Generate travel recommendations"""
        if not self.validate_inputs():
            return
        
        # Disable button and show loading
        self.generate_btn.config(state='disabled')
        self.loading_label.config(text="🔄 Generating luxury recommendations... This may take a moment.")
        
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._generate_recommendations_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_recommendations_thread(self):
        """Thread function for generating recommendations"""
        try:
            destination = self.destination_var.get().strip()
            start_date = self.start_date.get_date().strftime("%Y-%m-%d")
            end_date = self.end_date.get_date().strftime("%Y-%m-%d")
            
            # Generate recommendations
            recommendations = self.travel_assistant.generate_recommendations(
                destination, start_date, end_date
            )
            
            # Update UI in main thread
            self.root.after(0, self._update_results, recommendations, destination, start_date, end_date)
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
    
    def _update_results(self, recommendations, destination, start_date, end_date):
        """Update the results display"""
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        
        if "error" in recommendations:
            self.results_text.insert('1.0', f"⚠️ {recommendations['error']}\n\n")
            # Still show any available recommendations
            if recommendations.get('destination_overview'):
                content = self._format_recommendations(recommendations, destination, start_date, end_date)
                self.results_text.insert(tk.END, content)
        else:
            # Format and display recommendations
            content = self._format_recommendations(recommendations, destination, start_date, end_date)
            self.results_text.insert('1.0', content)
        
        self.results_text.config(state='disabled')
        
        # Re-enable button and hide loading
        self.generate_btn.config(state='normal')
        self.loading_label.config(text="✅ Recommendations generated successfully!")
    
    def _show_error(self, error_msg):
        """Show error message"""
        self.generate_btn.config(state='normal')
        self.loading_label.config(text="❌ Error generating recommendations")
        messagebox.showerror("Error", error_msg)
    
    def _format_recommendations(self, recommendations, destination, start_date, end_date):
        """Format recommendations for display"""
        content = f"🏖️ LUXURY TRAVEL RECOMMENDATIONS\n"
        content += f"📍 Destination: {destination}\n"
        content += f"📅 Travel Dates: {start_date} to {end_date}\n"
        content += "="*80 + "\n\n"
        
        # If there's a raw AI response, show it first
        if recommendations.get('raw_ai_response'):
            content += f"🤖 AI RECOMMENDATIONS\n"
            content += recommendations['raw_ai_response'] + "\n\n"
            content += "="*80 + "\n\n"
        
        # Destination Overview
        if recommendations.get('destination_overview'):
            content += f"🌟 DESTINATION OVERVIEW\n"
            content += f"{recommendations['destination_overview']}\n\n"
        
        # Weather
        if recommendations.get('weather'):
            content += f"🌤️ WEATHER & PACKING\n"
            content += f"{recommendations['weather']}\n\n"
        
        # Luxury Hotels
        if recommendations.get('luxury_hotels'):
            content += "🏨 LUXURY ACCOMMODATIONS\n"
            content += "-" * 40 + "\n"
            for i, hotel in enumerate(recommendations['luxury_hotels'], 1):
                if isinstance(hotel, dict):
                    content += f"{i}. {hotel.get('name', 'N/A')}\n"
                    content += f"   💰 Price: {hotel.get('price_range', 'Contact for rates')}\n"
                    content += f"   📝 {hotel.get('description', '')}\n\n"
                else:
                    content += f"{i}. {hotel}\n\n"
        
        # Fine Dining
        if recommendations.get('fine_dining'):
            content += "🍽️ FINE DINING EXPERIENCES\n"
            content += "-" * 40 + "\n"
            for i, restaurant in enumerate(recommendations['fine_dining'], 1):
                if isinstance(restaurant, dict):
                    content += f"{i}. {restaurant.get('name', 'N/A')}\n"
                    content += f"   🍳 Cuisine: {restaurant.get('cuisine_type', 'N/A')}\n"
                    content += f"   💰 Price: {restaurant.get('price_range', 'Contact for rates')}\n"
                    content += f"   📝 {restaurant.get('description', '')}\n\n"
                else:
                    content += f"{i}. {restaurant}\n\n"
        
        # Exclusive Experiences
        if recommendations.get('exclusive_experiences'):
            content += "✨ EXCLUSIVE EXPERIENCES\n"
            content += "-" * 40 + "\n"
            for i, experience in enumerate(recommendations['exclusive_experiences'], 1):
                if isinstance(experience, dict):
                    content += f"{i}. {experience.get('name', 'N/A')}\n"
                    content += f"   💰 Price: {experience.get('price_range', 'Contact for rates')}\n"
                    content += f"   📝 {experience.get('description', '')}\n\n"
                else:
                    content += f"{i}. {experience}\n\n"
        
        # Luxury Shopping
        if recommendations.get('luxury_shopping'):
            content += "🛍️ LUXURY SHOPPING\n"
            content += "-" * 40 + "\n"
            for i, shopping in enumerate(recommendations['luxury_shopping'], 1):
                if isinstance(shopping, dict):
                    content += f"{i}. {shopping.get('name', 'N/A')}\n"
                    content += f"   🏪 Type: {shopping.get('type', 'N/A')}\n"
                    content += f"   📝 {shopping.get('description', '')}\n\n"
                else:
                    content += f"{i}. {shopping}\n\n"
        
        # Transportation
        if recommendations.get('transportation'):
            content += "🚗 LUXURY TRANSPORTATION\n"
            content += "-" * 40 + "\n"
            for i, transport in enumerate(recommendations['transportation'], 1):
                if isinstance(transport, dict):
                    content += f"{i}. {transport.get('type', 'N/A')}\n"
                    content += f"   📝 {transport.get('description', '')}\n\n"
                else:
                    content += f"{i}. {transport}\n\n"
        
        # Seasonal Highlights
        if recommendations.get('seasonal_highlights'):
            content += "🎭 SEASONAL HIGHLIGHTS\n"
            content += "-" * 40 + "\n"
            for i, highlight in enumerate(recommendations['seasonal_highlights'], 1):
                content += f"{i}. {highlight}\n"
            content += "\n"
        
        # Insider Tips
        if recommendations.get('insider_tips'):
            content += "💡 INSIDER TIPS\n"
            content += "-" * 40 + "\n"
            for i, tip in enumerate(recommendations['insider_tips'], 1):
                content += f"{i}. {tip}\n"
            content += "\n"
        
        content += "="*80 + "\n"
        content += "Generated by AI-Powered Luxury Travel Assistant"
        
        return content

def main():
    root = tk.Tk()
    app = TravelAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()