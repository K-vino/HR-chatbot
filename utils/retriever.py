import os
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from utils.embedder import load_vector_db
import torch

def get_local_llm():
    """
    Initialize a local open-source LLM using HuggingFace
    Using a lightweight model that works well for Q&A tasks
    """
    model_name = "microsoft/DialoGPT-medium"  # Lightweight conversational model
    # Alternative: "distilbert-base-cased-distilled-squad" for Q&A specific

    try:
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,  # Use float32 for CPU compatibility
            device_map="auto" if torch.cuda.is_available() else None
        )

        # Create pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            temperature=0.7,
            do_sample=True,
            device=0 if torch.cuda.is_available() else -1  # GPU if available, else CPU
        )

        # Wrap in LangChain
        llm = HuggingFacePipeline(pipeline=pipe)
        return llm

    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        # Fallback to a simpler model
        return get_fallback_llm()

def get_fallback_llm():
    """
    Fallback to a very lightweight model for systems with limited resources
    """
    try:
        from transformers import pipeline

        # Use a smaller, CPU-friendly model
        pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            device=-1  # Force CPU
        )

        llm = HuggingFacePipeline(pipeline=pipe)
        return llm

    except Exception as e:
        print(f"Error with fallback model: {e}")
        return None

def get_hr_prompt_template():
    """
    Create an HR-specific prompt template for better responses
    """
    template = """
    You are an HR Assistant chatbot. Use the following context from HR documents to answer the question.
    Be helpful, professional, and accurate. If you don't know the answer based on the context, say so.

    Context from HR documents:
    {context}

    Question: {question}

    HR Assistant Answer:"""

    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

def get_qa_chain():
    """
    Create a QA chain using open-source components
    """
    # Load vector database
    vector_db = load_vector_db()

    if vector_db is None:
        return None

    # Get retriever
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # Retrieve top 3 relevant chunks
    )

    # Get local LLM
    llm = get_local_llm()

    if llm is None:
        return None

    # Create QA chain with custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": get_hr_prompt_template()
        }
    )

    return qa_chain

def simple_qa_response(question, max_retries=2):
    """
    Simple Q&A function with error handling and retries
    """
    for attempt in range(max_retries):
        try:
            qa_chain = get_qa_chain()
            if qa_chain is None:
                return "Sorry, the HR assistant is currently unavailable. Please try again later."

            result = qa_chain({"query": question})
            return result["result"]

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return "I'm having trouble processing your question right now. Please try rephrasing or contact HR directly."

    return "Service temporarily unavailable."
