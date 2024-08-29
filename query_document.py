import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai

from get_embedding import get_embedding_function
import api_key
GOOGLE_API_KEY = api_key.GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Explain the document in detail:

{context}

---

Based on the above, give detailed explanations for each section.: {question}
"""

SUMMARY_PROMPT_TEMPLATE = """
:

{context}

---

Summary:
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, nargs="?", help="The query text.")
    parser.add_argument("--summarize", action="store_true", help="Summarize all documents in the database.")
    args = parser.parse_args()

    if args.summarize:
        summarize_database()
    elif args.query_text:
        query_text = args.query_text
        query_rag(query_text.text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response_text = model.generate_content(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(response_text.text)
    return response_text

def summarize_database():
    # Load the Chroma DB
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    
    # Retrieve all documents from the database
    documents = db.get(include=["documents", "metadatas"])["documents"]
    
    if not documents:
        print("No documents found in the database to summarize.")
        return
    
    # Combine all document content
    context_text = "\n\n---\n\n".join(doc for doc in documents)

    # Prepare the summarization prompt
    prompt_template = ChatPromptTemplate.from_template(SUMMARY_PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text)

    # Summarize using the model
    model = genai.GenerativeModel("gemini-1.5-flash")
    response_text = model.generate_content(prompt)

    # Print the summary
    print(response_text.text)
    return response_text.text



if __name__ == "__main__":
    main()
