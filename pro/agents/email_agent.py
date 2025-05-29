from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pro.model.Flowbit import FlowbitSchema
from langchain.memory.entity import RedisEntityStore
from dotenv import load_dotenv
load_dotenv()
redis_url = "redis://default:JH2VrZk4jZgPAW97uhVupTjSjajxdLrP@redis-11052.c44.us-east-1-2.ec2.redns.redis-cloud.com:11052"
entity_store = RedisEntityStore(redis_url=redis_url)
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash-8b')
model_with_stuctured_output=model.with_structured_output(FlowbitSchema)
prompt = PromptTemplate(
    template='this is the email from our client u need to extract the details from the email and give a structured output {email}',
    input_variables=['email']
)

def set_memory_input(input_dict):
    email_id=input_dict['email']
    email_text = input_dict['data']



email_chain=prompt|model_with_stuctured_output
email_agent = email_chain