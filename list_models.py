import google.generativeai as genai
LLM_KEY = "AIzaSyBr5tbI8lTxjThWaONAYSUvgBBwzc3URiI"
genai.configure(api_key=LLM_KEY)
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(e)
