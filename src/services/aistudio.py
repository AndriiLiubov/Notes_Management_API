import google.generativeai as genai
import os
from dotenv import load_dotenv

# upload API key from .env
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# configurate Google Gemini AI
genai.configure(api_key=GENAI_API_KEY)

def summarize_text(text: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Summarize this note: {text}")
    
    return response.text if response else "Summary not available."
