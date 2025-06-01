from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableBranch,RunnableLambda
from project.model.Classify import  ClassifySchema
from project.agents.email_agent import email_chain, stream_email_agent
from project.agents.json_agent import json_chain, stream_json_agent
import json
import os
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
model_with_structured_output=model.with_structured_output(ClassifySchema)

prompt = PromptTemplate(
    template="""
You are a classification assistant. Your task is to detect:

1. The format of the input (one of: 'email', 'json', 'pdf')
2. The business intent (one of: 'RFQ', 'Complaint', 'Invoice', 'Regulation', 'Fraud Risk')
3. Extract the email address if present (else leave it empty)
4. Extract the core content or structured data

Use the following examples as reference:
Example 1:
Input:
Subject: Request for Quotation
From: sales@acme.com
Body: Hello, please send us a quote for 200 widgets.
Output:
{{
  "type": "email",
  "intent": "RFQ",
  "email": "sales@acme.com",
  "data": "Request for quotation for 200 widgets"
}}
Example 2:
Input:
{{
  "source": "webhook",
  "message": "Urgent complaint received from customer ID 3289"
}}
Output:
{{
  "type": "json",
  "intent": "Complaint",
  "email": "",
  "data": "Urgent complaint received from customer ID 3289"
}}
Example 3:
Input:
PDF content:
"Invoice #8452
Total Amount: $12,500
Due: 15th April 2025"

Output:
{{
  "type": "pdf",
  "intent": "Invoice",
  "email": "",
  "data": "Invoice total $12,500 due 15th April 2025"
}}
Now classify the following input:
{inp}
""",
    input_variables=["inp"]
)
branch_chain = RunnableBranch(
    (lambda x: x.type == 'email', RunnableLambda(lambda x: {"email": x.email,"data":x.data}) | email_chain),
    (lambda x: x.type == 'json', RunnableLambda(lambda x: {"email":x.email,"data": x.data}) | json_chain),
    RunnableLambda(lambda x: {"error": "Unsupported format"})
)

classifier_chain= prompt|model_with_structured_output
main_chain = classifier_chain|branch_chain
classifier_agent = classifier_chain
main_agent = main_chain

def stream_main_agent(input_data: dict):
    inp = input_data.get("inp", "").strip()
    if not inp:
        yield " No input provided.\n\n\n\n\n\n\n\n\n\n"
        return

    yield "🔍 Step 1: Formatting classifier prompt...\n\n\n\n\n\n\n\n\n\n"
    formatted_prompt = prompt.format(inp=inp)
    yield " Step 2: Calling Gemini classifier...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    try:
        result = model_with_structured_output.invoke(formatted_prompt)
    except Exception as e:
        yield f" Classifier model error: {e}\n"
        return

    output = result.model_dump()
    yield " Step 3: Classification result:\n"
    yield json.dumps(output, indent=2) + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

    typ = output.get("type")
    email = output.get("email")
    data = output.get("data")

    if typ == "email":
        yield " Step 4: Routing to Email Agent...\n\n\n\n\n\n\n\n\n\n"
        for step in stream_email_agent({"email": email, "data": data}):
            yield " [Email Agent] " + step
    elif typ == "json":
        yield " Step 4: Routing to JSON Agent...\n\n\n\n\n\n\n\n\n\n\n"
        for step in stream_json_agent({"email": email, "data": data}):
            yield " [JSON Agent] " + step
    else:
        yield " Unsupported input type. Only 'email' and 'json' are supported.\n"

    yield " Done.\n"
