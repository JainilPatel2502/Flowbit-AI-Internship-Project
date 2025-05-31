import json
import time
import os
import requests
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory.entity import RedisEntityStore
from pro.model.Flowbit import FlowbitSchema
from pro.memory.memory import set_memory,get_memory
load_dotenv()

prompt = PromptTemplate(
    template="""
    This is a JSON blob from our client. Extract structured details.

    Conversation history:
    {history}

    New JSON:
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
        "output": result,
        "raw_history": inputs["raw_history"]
    }

run_model = RunnableLambda(run_model_fn)
jsonchain = format_prompt | run_model
json_chain = get_memory | format_prompt | run_model | set_memory
json_agent = json_chain
json_ch=prompt|model_with_structured_output
json_agent = json_ch

def stream_json_agent(input_data: dict):
    memory = get_memory.invoke(input_data)
    yield f"Step 5: Memory fetched -> {memory}\n"

    formatted = prompt.format(input=memory["input"], history=memory["history"])
    yield f"Step 6: Prompt formatted -> {formatted}\n"

    model_output = model_with_structured_output.invoke(formatted)
    output_json = model_output.model_dump()
    result = output_json
    yield f"Step 7: Model called -> {json.dumps(output_json, indent=2)}\n"
    if result['tone']=="angry":
        response=requests.get("http://127.0.0.1:8001/risk_alert",json={"tone":result['tone'],"email":result['customer']["email"]})

    if result['tone']=="extreamly angry":
        response=requests.get("http://127.0.0.1:8001/risk_alert",json={"tone":result['tone'],"email":result['customer']["email"]})

    if result['total']>10000:
        response=requests.get("http://127.0.0.1:8001/total",json={"total":result['total'],"email":result['customer']["email"]})
    full_output = {
        "email": input_data["email"],
        "input": input_data["data"],
        "output": output_json,
        "raw_history": memory["raw_history"]
    }
    set_memory.invoke(full_output)
    yield f"Step 8: Memory saved.\n"

    yield f" Done.\n"