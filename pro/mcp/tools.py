from langchain.tools import tool
from pro.agents.classifier_agent import classifier_chain
from pro.agents.pdf_agent import pdf_chain, extract_text_from_pdf
from pro.agents.email_agent import emailchain
from pro.memory.memory import get_history_from_redis,set_history_to_redis
from pro.agents.json_agent import jsonchain


@tool
def classify_tool(input: str) -> dict:
    """Classify the input to detect format (email/json) and intent (RFQ, Complaint, Invoice, etc)."""
    return classifier_chain.invoke({'inp': input})

@tool
def email_tool(email: str, data: str, intent: str = None) -> dict:
    """Processes an email input using memory-aware chain."""
    history_text, raw_history = get_history_from_redis(email, data)
    prompt_input = {
        "email": email,
        "input": data,
        "history": history_text,  # Fixed: Using the formatted history text
        "raw_history": raw_history
    }
    result = emailchain.invoke(prompt_input)
    set_history_to_redis(email, data, result, raw_history)
    return result

@tool
def json_tool(email: str, data: str, intent: str = None) -> dict:
    """Processes a JSON webhook input using memory-aware chain."""
    history_text, raw_history = get_history_from_redis(email, data)
    prompt_input = {
        "email": email,
        "input": data,
        "history": history_text,  # Added missing history parameter
        "raw_history": raw_history
    }
    result = jsonchain.invoke(prompt_input)
    set_history_to_redis(email, data, result, raw_history)
    return result

@tool
def pdf_tool(path: str, email: str = None) -> dict:
    """Process and extract structured information from a PDF file path."""
    text = extract_text_from_pdf(path)
    
    # If no email is provided, use the path as a unique identifier
    email_id = email if email else f"pdf_{path}"
    
    history_text, raw_history = get_history_from_redis(email_id, text)
    prompt_input = {
        "email": email_id,
        "input": text,  # Using the extracted text
        "history": history_text,
        "raw_history": raw_history
    }
    
    result = pdf_chain.invoke(prompt_input)
    set_history_to_redis(email_id, text, result, raw_history)
    return result