import os
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Initialize open-source embedding model
def get_embedding_model():
    """Get the open-source embedding model"""
    model_name = "all-MiniLM-L6-v2"  # Lightweight and efficient
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
        encode_kwargs={'normalize_embeddings': True}
    )

def create_vector_db(chunks, collection_name="hr_documents"):
    """
    Create a ChromaDB vector database from text chunks
    Args:
        chunks (List[str]): List of text chunks
        collection_name (str): Name for the ChromaDB collection
    """
    # Create documents from chunks
    docs = [Document(page_content=chunk, metadata={"chunk_id": i})
            for i, chunk in enumerate(chunks)]

    # Initialize embedding model
    embeddings = get_embedding_model()

    # Create ChromaDB vector store
    persist_directory = "vectorstore"
    os.makedirs(persist_directory, exist_ok=True)

    # Create or update the vector database
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )

    # Persist the database
    vectordb.persist()

    return vectordb

def load_vector_db(collection_name="hr_documents"):
    """
    Load existing ChromaDB vector database
    Args:
        collection_name (str): Name of the ChromaDB collection
    Returns:
        Chroma: The loaded vector database
    """
    persist_directory = "vectorstore"
    embeddings = get_embedding_model()

    if os.path.exists(persist_directory):
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name=collection_name
        )
        return vectordb
    else:
        return None
