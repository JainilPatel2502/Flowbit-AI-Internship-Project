from dotenv import load_dotenv
import  os
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
# Use LangChain's PyPDFLoader to extract text
def extract_text_from_pdf(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text = " ".join([page.page_content for page in pages])
    return text.strip()

# Format the prompt
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

