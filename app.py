import streamlit as st
import os
from utils.loader import load_pdf_chunks
from utils.embedder import create_vector_db
from utils.retriever import get_qa_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
st.set_page_config(page_title="HR Chatbot - RAG App", layout="centered")

# Title
st.title("💼 HR Assistant Chatbot")
st.write("Ask any question related to HR policies and get instant answers based on uploaded documents.")

# Handle file upload
uploaded_file = st.file_uploader("📄 Upload HR Policy Document (PDF only)", type=["pdf"])

# Create directories if not present
os.makedirs("data", exist_ok=True)
os.makedirs("vectorstore", exist_ok=True)

if uploaded_file:
    file_path = os.path.join("data", uploaded_file.name)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("📚 Processing and indexing document..."):
        chunks = load_pdf_chunks(file_path)
        create_vector_db(chunks)
    st.success("✅ Document processed and stored in vector DB!")

st.markdown("---")

# Q&A Interface
if os.path.exists("vectorstore"):
    user_input = st.text_input("💬 Ask an HR-related question:")

    if st.button("🔎 Get Answer") and user_input:
        with st.spinner("🤖 Thinking..."):
            qa_chain = get_qa_chain()
            response = qa_chain.run(user_input)
        st.markdown("### ✅ Answer:")
        st.write(response)
else:
    st.info("📂 Please upload a document to begin chatting.")
