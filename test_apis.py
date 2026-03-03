import google.generativeai as genai
from duckduckgo_search import DDGS
import os

# Mock ASSISTANT_NAME
ASSISTANT_NAME = "jarvis"
LLM_KEY = "AIzaSyBr5tbI8lTxjThWaONAYSUvgBBwzc3URiI"

print("--- Testing Gemini ---")
try:
    genai.configure(api_key=LLM_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello")
    print("Gemini Response:", response.text)
except Exception as e:
    print("Gemini Error:", e)

print("\n--- Testing DuckDuckGo ---")
try:
    with DDGS() as ddgs:
        results = list(ddgs.text("PM of India now", max_results=3))
        print("DDG Results:", results)
except Exception as e:
    print("DDG Error:", e)
