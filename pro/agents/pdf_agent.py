from dotenv import load_dotenv
import  os
import json
import time
import requests
from pydantic import BaseModel
from langchain.schema.runnable import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory.entity import RedisEntityStore
from langchain_community.document_loaders import PyPDFLoader
from pro.model.Classify import Email
from pro.model.Flowbit import FlowbitSchema
from pro.memory.memory import set_memory, get_memory
load_dotenv()

initial_prompt=PromptTemplate(
    template='here is  the text  from a pdf iddentify the  email address and the intent of the text data : {data}',
    input_variables=['data']
)
# Define the prompt for PDF input
prompt = PromptTemplate(
    template="""
    This is a PDF document from our client. Extract structured details.

    Conversation history:
    {history}

    New PDF content:
    {input}
    """,
    input_variables=["input", "history"]
)
# Gemini model with FlowbitSchema output
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

model_with_structured_output = model.with_structured_output(FlowbitSchema)
model_email=model.with_structured_output(Email)

email_chain = initial_prompt|model_email
def extract_text_from_pdf(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text = " ".join([page.page_content for page in pages])
    return text.strip()

def format_prompt_fn(inputs: dict) -> dict:
    formatted = prompt.format(input=inputs["input"], history=inputs["history"])
    print("Prompt formatted")
    return {
        "email": inputs["email"],
        "input": inputs["input"],
        "formatted_prompt": formatted,
        "raw_history": inputs["raw_history"]
    }

format_prompt = RunnableLambda(format_prompt_fn)

def model_to_dict_fn(model:Email)->dict:
    return model.model_dump()
model_to_dict=RunnableLambda(model_to_dict_fn)

# Run the model
def run_model_fn(inputs: dict) -> dict:
    result = model_with_structured_output.invoke(inputs["formatted_prompt"])
    print("Model thinking")
    return {
        "email": inputs["email"],
        "input": inputs["input"],
        "output": result,
        "raw_history": inputs["raw_history"]
    }

run_model = RunnableLambda(run_model_fn)

pdfchain=format_prompt | run_model
pdf_chain = initial_prompt|model_email|model_to_dict|get_memory | format_prompt | run_model | set_memory
pdf_agent = pdf_chain

def pdf_stream_agent(pdf_path: str):
    yield " Extracting text from PDF...\n\n\n"
    text = extract_text_from_pdf(pdf_path)
    time.sleep(0.1)

    yield f"Extracted text\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n  {text}"
    email_data = email_chain.invoke({"data": text})
    email_data=email_data.model_dump()
    email = email_data['email']
    intent = email_data['intent']
    time.sleep(0.1)

    yield f"Pdf recived from the email id {email} whith an intent of {intent}\n \n\n\n\n\n\n\n\n\n\n  "

    yield f"Serching in memory for any previous mails\n \n\n\n\n\n\n\n\n\n\n \n \n\n\n\n\n\n\n\n\n\n  "
    raw_history = get_memory.invoke(email_data)
    time.sleep(0.1)
    if raw_history:
        yield f"found {raw_history}\n \n\n\n\n\n\n\n\n\n\n \n \n\n\n\n\n\n\n\n\n\n "
    
    formatted_prompt = prompt.format(input=text, history=raw_history)
    time.sleep(0.1)

    yield f"Pdf agent exptracting the data\n \n\n\n\n\n\n\n\n\n\n \n \n\n\n\n\n\n\n\n\n\n "
    result = model_with_structured_output.invoke(formatted_prompt)
    time.sleep(0.1)

    if result['tone']=="angry":
        response=requests.get("http://127.0.0.1:8001/risk_alert",json={"tone":result['tone'],"email":result['customer']["email"]})

    if result['tone']=="extreamly angry":
        response=requests.get("http://127.0.0.1:8001/risk_alert",json={"tone":result['tone'],"email":result['customer']["email"]})

    if result['total']>10000:
        response=requests.get("http://127.0.0.1:8001/total",json={"total":result['total'],"email":result['customer']["email"]})

    yield f"Saving in memory\n \n\n\n\n\n\n\n\n\n\n "
    full_output = {
        "email": email,
        "input": text,
        "output": result.model_dump(),
        "raw_history": raw_history["raw_history"]
    }
    set_memory.invoke(full_output)
    time.sleep(0.1)

    yield f"\n \n\n\n\n\n\n\n\n\n\n {json.dumps(result.model_dump(), indent=2)}"