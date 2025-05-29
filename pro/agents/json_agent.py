from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pro.model.Flowbit import FlowbitSchema
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash-8b')
model_with_stuctured_output=model.with_structured_output(FlowbitSchema)
prompt = PromptTemplate(
    template='this is the json from our client u need to extract the details from the json and give a structured output {json}',
    input_variables=['json']
)
json_chain=prompt|model_with_stuctured_output
json_agent = json_chain