from duckduckgo_search import DDGS
import google.generativeai as genai
import sys

LLM_KEY = "AIzaSyBr5tbI8lTxjThWaONAYSUvgBBwzc3URiI"

print("Gemini Test...")
try:
    genai.configure(api_key=LLM_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say 'Gemini is working'")
    print("Response:", response.text)
except Exception as e:
    print("Gemini Failed:", e)

print("\nDDG Test...")
try:
    with DDGS() as ddgs:
        for r in ddgs.text("Narendra Modi", max_results=1):
            print("DDG:", r)
except Exception as e:
    print("DDG Failed:", e)
