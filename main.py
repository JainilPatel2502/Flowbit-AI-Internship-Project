import streamlit as st
import requests
import json

# MCP server endpoint
MCP_SERVER_URL = "http://localhost:8000/mcp/route"  # update if your route is different

st.set_page_config(page_title="MCP AI Agent", layout="wide")
st.title("🧠 Multi-Format Intake Agent with Context Memory")

# Tabs for input modes
tab_email, tab_json, tab_pdf = st.tabs(["📧 Email Input", "🧾 JSON Input", "📄 PDF Upload"])

with tab_email:
    st.header("Email Input")
    email = st.text_input("Sender Email")
    message = st.text_area("Email Content")
    intent = st.selectbox("Intent (optional)", ["", "RFQ", "Complaint", "Invoice", "Feedback"])
    
    if st.button("Submit Email", key="submit_email"):
        if not email or not message:
            st.warning("Email and message are required.")
        else:
            payload = {
                "type": "email",
                "email": email,
                "data": message,
                "intent": intent or "unknown"
            }
            with st.spinner("Thinking..."):
                res = requests.post(MCP_SERVER_URL, json=payload)
                st.success("Response received")
                st.json(res.json())

with tab_json:
    st.header("JSON Webhook Input")
    email = st.text_input("Sender Email (for memory tracking)", key="json_email")
    json_data = st.text_area("Paste JSON Payload", height=200)
    intent = st.selectbox("Intent (optional)", ["", "RFQ", "Complaint", "Invoice", "Feedback"], key="json_intent")
    
    if st.button("Submit JSON", key="submit_json"):
        if not email or not json_data:
            st.warning("Both email and JSON are required.")
        else:
            try:
                parsed_data = json.loads(json_data)
                payload = {
                    "type": "json",
                    "email": email,
                    "data": str(parsed_data),  # flatten if needed
                    "intent": intent or "unknown"
                }
                with st.spinner("Processing..."):
                    res = requests.post(MCP_SERVER_URL, json=payload)
                    st.success("Response received")
                    st.json(res.json())
            except json.JSONDecodeError:
                st.error("Invalid JSON format")

with tab_pdf:
    st.header("PDF Upload")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if st.button("Submit PDF"):
        if uploaded_file:
            files = {"file": uploaded_file.getvalue()}
            with st.spinner("Extracting text and analyzing..."):
                res = requests.post("http://localhost:8000/mcp/pdf", files={"pdf": uploaded_file})
                st.success("Response received")
                st.json(res.json())
        else:
            st.warning("Please upload a PDF.")
