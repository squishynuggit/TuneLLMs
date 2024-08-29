import api_key
GOOGLE_API_KEY = api_key.GOOGLE_API_KEY

import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Describe what a RAG is and how to implement one.")
print(response.text)