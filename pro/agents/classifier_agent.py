from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableBranch,RunnableLambda
from pro.model.Classify import  ClassifySchema
from pro.agents.email_agent import email_chain
from pro.agents.json_agent import json_chain
import json
import os
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

model_with_structured_output=model.with_structured_output(ClassifySchema)
input="""Subject: Request for Quotation - Bulk Purchase from:patelson222@gmail.com Hi
payment stil not done please do it in very urgent manner or else you may face serious legal issues
Regards,  
Priya Shah  
Test Business Team, Test Business Ltd.
"""

# input="""{
#     "email":"jsainilpatel2222@gmail.com",
#   "invoice_id": "INV-2024-0012",
#   "date": "2024-06-10",
#   "customer": {
#     "name": "GreenTech Solutions",
#     "email": "billing@greentech.com"
#   },
#   "items": [
#     {
#       "description": "Solar Panel - 250W",
#       "quantity": 10,
#       "unit_price": 150
#     },
#     {
#       "description": "Inverter - 3kW",
#       "quantity": 2,
#       "unit_price": 500
#     }
#   ],
#   "total_amount": 2500,
#   "currency": "USD"
# }
# """


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