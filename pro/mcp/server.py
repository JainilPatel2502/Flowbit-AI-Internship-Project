from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType
from pro.mcp.tools import classify_tool, email_tool, json_tool, pdf_tool
import os
import uuid

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

tools = [email_tool, json_tool, pdf_tool, classify_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,  
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

class TextInput(BaseModel):
    input: str

@app.post("/process-text")
async def process_text(input_data: TextInput):
    """Process any text-based input (email, JSON, plain text)"""
    try:
        print("hi")
        result = agent.run(input_data.input)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...), email: str = Form(...)):
    """Process PDF files with email identifier for memory"""
    try:
        # Create temporary file
        filename = f"tmp_{uuid.uuid4()}.pdf"
        file_path = f"/tmp/{filename}"
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process with agent
        result = agent.run(f"This is a PDF file at {file_path} for user {email}.")
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {"result": result}
    except Exception as e:
        # Ensure cleanup on error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return {"error": str(e)}

@app.get("/")
def root():
    return {"status": "ready"}