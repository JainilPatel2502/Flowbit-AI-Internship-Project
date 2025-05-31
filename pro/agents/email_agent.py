import json
import time
import os
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory.entity import RedisEntityStore
from pro.model.Flowbit import FlowbitSchema
from pro.memory.memory import get_memory,set_memory
load_dotenv()

prompt = PromptTemplate(
    template="""
    This is the email from our client. Extract structured details.

    Conversation history:
    {history}

    New message:
    {input}
    """,
    input_variables=["input", "history"]
)

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

model_with_structured_output = model.with_structured_output(FlowbitSchema)

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

def run_model_fn(inputs: dict) -> dict:
    result = model_with_structured_output.invoke(inputs["formatted_prompt"])
    print("Model thinking")
    return {
        "email": inputs["email"],
        "input": inputs["input"],
        "output": result.model_dump(),
        "raw_history": inputs["raw_history"]
    }

run_model = RunnableLambda(run_model_fn)

#email
emailchain=format_prompt | run_model

#memory
email_chain = get_memory | format_prompt | run_model | set_memory

#basic
email_ch=prompt|model_with_structured_output
email_agent = email_ch