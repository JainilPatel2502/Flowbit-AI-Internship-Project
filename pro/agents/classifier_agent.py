from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableBranch,RunnableLambda
from pro.model.Classify import  ClassifySchema
from pro.agents.email_agent import email_chain
from pro.agents.json_agent import json_chain
import json
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash-8b')
model_with_structured_output=model.with_structured_output(ClassifySchema)
input="""Subject: Request for Quotation - Bulk Purchase from:jainilpatel2222@gmail.com Hi
We are looking to place a bulk order for electronic components including resistors, capacitors, and ICs. Could you please send us a quotation with pricing and delivery time?
Regards,  
Priya Shah  
Procurement Team, TechParts Ltd.
"""
prompt=PromptTemplate(
    template='{inp}',
    input_variables=['inp']
)
branch_chain = RunnableBranch(
    (lambda x: x.type == 'email', RunnableLambda(lambda x: {"email": x.data}) | email_chain),
    (lambda x: x.type == 'json', RunnableLambda(lambda x: {"json": x.data}) | json_chain),
    RunnableLambda(lambda x: {"error": "Unsupported format"})
)

classifier_chain= prompt|model_with_structured_output
main_chain = classifier_chain|branch_chain
classifier_agent = classifier_chain
main_agent = main_chain
# res=main_chain.invoke({"inp":input})
# print(type(res))
# json_out=res.model_dump()
# with open('output.json','w') as f:
    # json.dump(json_out,f,indent=3)
