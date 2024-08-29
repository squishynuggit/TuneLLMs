import api_key
GOOGLE_API_KEY = api_key.GOOGLE_API_KEY

from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding_function():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
    return embeddings