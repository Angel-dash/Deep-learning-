from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel ("models/gemini-1.5-flash")

