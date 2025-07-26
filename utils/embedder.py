import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

def create_vector_db(chunks):
    from langchain.schema import Document
    docs = [Document(page_content=chunk) for chunk in chunks]
    db = FAISS.from_documents(docs, embedding)
    db.save_local("vectorstore")
