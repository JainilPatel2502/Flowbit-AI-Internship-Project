# import streamlit as st
# import requests

# API_BASE = "http://localhost:8000"

# st.set_page_config(page_title="Grok-Like AI Agent", layout="centered")

# st.title("🤖 Multi-Format Agent Interface")

# tab1, tab2 = st.tabs(["📝 Text Input", "📄 PDF Upload"])

# with tab1:
#     st.subheader("Submit Email or JSON Text")
#     user_input = st.text_area("Enter your input", height=200)
#     if st.button("Process Text"):
#         if user_input.strip():
#             with st.spinner("🔄 Thinking..."):
#                 try:
#                     res = requests.post(f"{API_BASE}/process/", json={"inp": user_input})
#                     if res.status_code == 200:
#                         st.success("✅ Response:")
#                         st.json(res.json())
#                     else:
#                         st.error(f"❌ Error: {res.text}")
#                 except Exception as e:
#                     st.error(f"🚫 Could not connect: {e}")
#         else:
#             st.warning("Please enter some input.")

# with tab2:
#     st.subheader("Upload PDF File")
#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
#     if st.button("Process PDF"):
#         if uploaded_file:
#             with st.spinner("🔄 Thinking..."):
#                 try:
#                     files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
#                     res = requests.post(f"{API_BASE}/pdf/", files=files)
#                     if res.status_code == 200:
#                         st.success("✅ PDF Processed:")
#                         st.json(res.json())
#                     else:
#                         st.error(f"❌ Error: {res.text}")
#                 except Exception as e:
#                     st.error(f"🚫 Could not connect: {e}")
#         else:
#             st.warning("Please upload a PDF file.")





















# import streamlit as st
# import requests

# API_BASE = "http://localhost:8000"

# st.set_page_config(page_title="Grok-Like AI Agent", layout="centered")
# st.title("🤖 Multi-Format Agent Interface")

# tab1, tab2 = st.tabs(["📝 Text Input", "📄 PDF Upload"])
# with tab1:
#     st.subheader("Submit Email or JSON Text")
#     user_input = st.text_area("Enter your input", height=200)

#     if st.button("🧠 Stream Full Processing"):
#         if user_input.strip():
#             status_box = st.empty()
#             log_box = st.empty()
#             logs = ""

#             with status_box.container():
#                 st.info("🔄 Processing...")

#             try:
#                 with requests.post(f"{API_BASE}/stream/", json={"inp": user_input}, stream=True) as response:
#                     for line in response.iter_lines():
#                         if line:
#                             line_str = line.decode("utf-8")
#                             logs += f"{line_str}\n"
#                             log_box.code(logs, language="text")
#                 status_box.success("✅ Done")
#             except Exception as e:
#                 status_box.error(f"🚫 Could not connect: {e}")
#         else:
#             st.warning("Please enter some input.")







import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Grok-Like AI Agent", layout="centered")
st.title("🤖 Multi-Format Agent Interface")

tab1, tab2 = st.tabs(["📝 Text Input", "📄 PDF Upload"])

# TAB 1: Email or JSON Text
with tab1:
    st.subheader("Submit Email or JSON Text")
    user_input = st.text_area("Enter your input", height=200)

    if st.button("🧠 Stream Full Processing"):
        if user_input.strip():
            status_box = st.empty()
            log_box = st.empty()
            logs = ""

            with status_box.container():
                st.info("🔄 Processing...")

            try:
                with requests.post(f"{API_BASE}/stream/", json={"inp": user_input}, stream=True) as response:
                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode("utf-8")
                            logs += f"{line_str}\n"
                            log_box.code(logs, language="text")
                status_box.success("✅ Done")
            except Exception as e:
                status_box.error(f"🚫 Could not connect: {e}")
        else:
            st.warning("Please enter some input.")

# TAB 2: PDF Upload → /pdf/ API Call
with tab2:
    st.subheader("📄 Upload a PDF Document")

    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

    if uploaded_file:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        if st.button("🚀 Process PDF"):
            status_box = st.empty()
            stream_box = st.empty()
            logs = ""

            with status_box.container():
                st.info("🔄 Sending PDF to backend...")

            try:
                with open(temp_path, "rb") as f:
                    files = {"file": (uploaded_file.name, f, "application/pdf")}
                    with requests.post(f"{API_BASE}/pdf/", files=files, stream=True) as response:
                        for line in response.iter_lines():
                            if line:
                                line_str = line.decode("utf-8")
                                logs += f"{line_str}\n"
                                stream_box.code(logs, language="text")
                status_box.success("✅ Done")
            except Exception as e:
                status_box.error(f"🚫 PDF processing failed: {e}")
