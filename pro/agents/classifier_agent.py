from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableBranch,RunnableLambda
from pro.model.Classify import  ClassifySchema
from pro.agents.email_agent import email_chain, stream_email_agent
from pro.agents.json_agent import json_chain, stream_json_agent
import json
import os
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
model_with_structured_output=model.with_structured_output(ClassifySchema)

prompt=PromptTemplate(
    template='{inp}',
    input_variables=['inp']
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

# res=main_chain.invoke({"inp":input})
# with open('output.json','w') as f:
#     json.dump(res,f,indent=3)


def stream_main_agent(input_data: dict):
    inp = input_data.get("inp", "").strip()
    if not inp:
        yield "❌ No input provided.\n"
        return

    yield "🔍 Step 1: Formatting classifier prompt...\n"
    formatted_prompt = prompt.format(inp=inp)

    yield f"📨 Prompt:\n{formatted_prompt}\n"

    yield "🤖 Step 2: Calling Gemini classifier...\n"
    try:
        result = model_with_structured_output.invoke(formatted_prompt)
    except Exception as e:
        yield f"❌ Classifier model error: {e}\n"
        return

    output = result.model_dump()
    yield "✅ Step 3: Classification result:\n"
    yield json.dumps(output, indent=2) + "\n"

    typ = output.get("type")
    email = output.get("email")
    data = output.get("data")

    if typ == "email":
        yield "📬 Step 4: Routing to Email Agent...\n"
        for step in stream_email_agent({"email": email, "data": data}):
            yield "📨 [Email Agent] " + step
    elif typ == "json":
        yield "📦 Step 4: Routing to JSON Agent...\n"
        for step in stream_json_agent({"email": email, "data": data}):
            yield "🧾 [JSON Agent] " + step
    else:
        yield "❌ Unsupported input type. Only 'email' and 'json' are supported.\n"

    yield "✅ Done.\n"
