# from fastapi import FastAPI, HTTPException, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import tempfile
# import os
# import uuid
# from pro.agents.classifier_agent import main_agent
# from pro.agents.pdf_agent import extract_text_from_pdf  , pdf_agent

# app = FastAPI()

# class InputText(BaseModel):
#     inp: str

# @app.post("/process/")
# async def process_input(input_text: InputText):
#     try:
#         result = main_agent.invoke({"inp": input_text.inp})
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/pdf/")
# async def process_pdf(file: UploadFile = File(...)):
#     try:
#         # Use a safe cross-platform temp path
#         filename = f"tmp_{uuid.uuid4()}.pdf"
#         path = os.path.join(tempfile.gettempdir(), filename)
#         print(f"[INFO] Saving uploaded file to: {path}")

#         with open(path, "wb") as buffer:
#             content = await file.read()
#             print(f"[DEBUG] File content size: {len(content)} bytes")
#             buffer.write(content)

#         print("[INFO] Extracting text from PDF...")
#         text = extract_text_from_pdf(path)

#         print("[INFO] Invoking PDF agent...")
#         result = pdf_agent.invoke({'data': text})

#         os.remove(path)
#         return result

#     except Exception as e:
#         print(f"[ERROR] Exception occurred: {e}")
#         if 'path' in locals() and os.path.exists(path):
#             os.remove(path)
#         raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, Request,UploadFile, File
from fastapi.responses import StreamingResponse
from pro.agents.classifier_agent import stream_main_agent
from pro.agents.pdf_agent import pdf_stream_agent
import time
import uuid
import tempfile
import os

app = FastAPI()

# @app.post("/stream/")
# async def stream(request: Request):
#     data = await request.json()

#     def event_stream():
#         for step in stream_email_agent(data):
#             yield step
#             time.sleep(0.2)  # Simulated delay

#     return StreamingResponse(event_stream(), media_type="text/event-stream")
# from pro.agents.classifier_agent import stream_classifier_agent

@app.post("/stream/")
async def stream_all(request: Request):
    data = await request.json()

    def event_stream():
        for step in stream_main_agent(data):
            yield step
            time.sleep(0.05)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post('/pdf')
async def pdf(file: UploadFile = File(...)):
     
    filename = f"tmp_{uuid.uuid4()}.pdf"
    path = os.path.join(tempfile.gettempdir(), filename)
    print(f"[INFO] Saving uploaded file to: {path}")

    with open(path, "wb") as buffer:
        content = await file.read()
        print(f"[DEBUG] File content size: {len(content)} bytes")
        buffer.write(content)
    def event_stream():
        for step in pdf_stream_agent(path):
            yield step
            time.sleep(0.05)
    return StreamingResponse(event_stream(), media_type="text/event-stream")