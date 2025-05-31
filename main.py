import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Grok-Like AI Agent", layout="centered")

st.title("🤖 Multi-Format Agent Interface")

tab1, tab2 = st.tabs(["📝 Text Input", "📄 PDF Upload"])

with tab1:
    st.subheader("Submit Email or JSON Text")
    user_input = st.text_area("Enter your input", height=200)
    if st.button("Process Text"):
        if user_input.strip():
            with st.spinner("🔄 Thinking..."):
                try:
                    res = requests.post(f"{API_BASE}/process/", json={"inp": user_input})
                    if res.status_code == 200:
                        st.success("✅ Response:")
                        st.json(res.json())
                    else:
                        st.error(f"❌ Error: {res.text}")
                except Exception as e:
                    st.error(f"🚫 Could not connect: {e}")
        else:
            st.warning("Please enter some input.")

with tab2:
    st.subheader("Upload PDF File")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if st.button("Process PDF"):
        if uploaded_file:
            with st.spinner("🔄 Thinking..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    res = requests.post(f"{API_BASE}/pdf/", files=files)
                    if res.status_code == 200:
                        st.success("✅ PDF Processed:")
                        st.json(res.json())
                    else:
                        st.error(f"❌ Error: {res.text}")
                except Exception as e:
                    st.error(f"🚫 Could not connect: {e}")
        else:
            st.warning("Please upload a PDF file.")
