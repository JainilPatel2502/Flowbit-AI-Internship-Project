from fastapi import FastAPI, Request,UploadFile, File
from fastapi.responses import StreamingResponse
from pro.agents.classifier_agent import stream_main_agent
from pro.agents.pdf_agent import pdf_stream_agent
import time
import uuid
import tempfile
import os

app = FastAPI()

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

    with open(path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    def event_stream():
        for step in pdf_stream_agent(path):
            yield step
            time.sleep(0.05)
    return StreamingResponse(event_stream(), media_type="text/event-stream")