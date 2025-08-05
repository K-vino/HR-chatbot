import streamlit as st
import os
from utils.loader import load_pdf_chunks
from utils.embedder import create_vector_db, load_vector_db
from utils.retriever import simple_qa_response

st.set_page_config(
    page_title="HRBot - AI HR Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<h1 class="main-header">🤖 HRBot - AI HR Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent HR companion powered by open-source AI</p>', unsafe_allow_html=True)

# Sidebar for navigation and file upload
with st.sidebar:
    st.header("📁 Document Management")

    # File upload section
    uploaded_file = st.file_uploader(
        "Upload HR Policy Document",
        type=["pdf"],
        help="Upload PDF documents containing HR policies, handbooks, or guidelines"
    )

    # Show current documents
    if os.path.exists("data"):
        files = [f for f in os.listdir("data") if f.endswith('.pdf')]
        if files:
            st.subheader("📚 Uploaded Documents")
            for file in files:
                st.text(f"• {file}")

    st.markdown("---")
    st.subheader("ℹ️ About HRBot")
    st.info("""
    HRBot uses completely open-source AI models:
    • **LLM**: HuggingFace Transformers
    • **Embeddings**: Sentence Transformers
    • **Vector DB**: ChromaDB
    • **No API keys required!**
    """)

# Create directories if not present
os.makedirs("data", exist_ok=True)
os.makedirs("vectorstore", exist_ok=True)

# Handle file upload
if uploaded_file:
    file_path = os.path.join("data", uploaded_file.name)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("📚 Processing and indexing document... This may take a few minutes for the first run."):
        try:
            chunks = load_pdf_chunks(file_path)
            create_vector_db(chunks)
            st.markdown('<div class="success-box">✅ Document processed and stored in vector database!</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")

# Main chat interface
st.markdown("---")

# Check if vector database exists
vector_db = load_vector_db()
if vector_db is not None:
    st.subheader("💬 Ask Your HR Questions")

    # Sample questions
    with st.expander("💡 Sample Questions You Can Ask"):
        st.markdown("""
        • What is the company's leave policy?
        • How do I apply for maternity leave?
        • What are the working hours?
        • What is the dress code policy?
        • How does the performance review process work?
        • What benefits are available to employees?
        """)

    # Chat interface
    user_input = st.text_input(
        "Type your HR question here:",
        placeholder="e.g., What is the company's remote work policy?"
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        ask_button = st.button("🔎 Ask HRBot", type="primary")

    if ask_button and user_input:
        with st.spinner("🤖 HRBot is thinking... Please wait."):
            try:
                response = simple_qa_response(user_input)

                st.markdown("### 🤖 HRBot Response:")
                st.markdown(f'<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4;">{response}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Sorry, I encountered an error: {str(e)}")
                st.info("Please try rephrasing your question or contact HR directly.")

    # Quick actions
    st.markdown("---")
    st.subheader("🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Leave Policies"):
            st.session_state.quick_question = "What are the different types of leave available?"

    with col2:
        if st.button("💰 Benefits Info"):
            st.session_state.quick_question = "What employee benefits does the company offer?"

    with col3:
        if st.button("📞 Contact HR"):
            st.session_state.quick_question = "How can I contact the HR department?"

    # Handle quick questions
    if hasattr(st.session_state, 'quick_question'):
        with st.spinner("🤖 Processing quick question..."):
            response = simple_qa_response(st.session_state.quick_question)
            st.markdown("### 🤖 HRBot Response:")
            st.markdown(f'<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4;">{response}</div>', unsafe_allow_html=True)
        del st.session_state.quick_question

else:
    st.markdown('<div class="info-box">📂 Please upload an HR document to begin chatting with HRBot.</div>', unsafe_allow_html=True)

    st.subheader("🎯 What HRBot Can Do")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **📚 Document Analysis**
        • Process HR policies and handbooks
        • Extract key information automatically
        • Provide instant answers to policy questions

        **🔍 Smart Search**
        • Find relevant information quickly
        • Context-aware responses
        • No need to read through long documents
        """)

    with col2:
        st.markdown("""
        **🤖 AI-Powered Assistance**
        • 24/7 availability
        • Consistent and accurate responses
        • Learns from your HR documents

        **🔒 Privacy & Security**
        • All processing done locally
        • No data sent to external APIs
        • Your documents stay private
        """)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666; font-size: 0.9rem;">HRBot v1.0 - Powered by Open Source AI 🚀</p>',
    unsafe_allow_html=True
)
