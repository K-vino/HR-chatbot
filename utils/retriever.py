from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_qa_chain():
    vector_db = FAISS.load_local("vectorstore", ChatGoogleGenerativeAI(google_api_key=os.getenv("GEMINI_API_KEY")))
    retriever = vector_db.as_retriever()
    
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GEMINI_API_KEY"))
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    
    return chain
