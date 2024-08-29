import api_key
GOOGLE_API_KEY = api_key.GOOGLE_API_KEY

import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Describe what a RAG is and how to implement one.")
# print(response.text)

from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding_function():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
    return embeddings