import streamlit as st
import subprocess
import os
import time

# --- Setup ---
st.set_page_config(page_title="Convo Converter", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main .block-container { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        padding: 3rem; 
    }
    .stButton>button { background-color: white; color: black; font-weight: 700; width: 100%; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Convo")
st.write("Convert HWP to DOCX (Simple & Fast)")

uploaded_file = st.file_uploader("Upload your file", type=['hwp'])

if uploaded_file is not None:
    # Use a strictly alphanumeric filename
    in_file = "inputfile.hwp"
    out_file = "inputfile.docx"
    final_name = uploaded_file.name.replace(".hwp", ".docx")
    
    # Save the file
    with open(in_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # FORCE permissions (helps if the server is blocking the file)
    os.chmod(in_file, 0o777)

    bar = st.progress(0)
    status = st.empty()
    status.text("Converting...")

    try:
        # Use 'lowriter' specifically and force the 'writer8' filter for DOCX
        # This is a more 'aggressive' way to tell LibreOffice what to do
        cmd = [
            'soffice', 
            '--headless', 
            '--convert-to', 'docx:MS Word 2007 XML', 
            in_file
        ]
        
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

        # 3. Handle Result
        if os.path.exists(out_file):
            bar.progress(100)
            status.success("Conversion Successful!")
            with open(out_file, "rb") as f:
                st.download_button(
                    label="DOWNLOAD DOCX",
                    data=f,
                    file_name=final_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            st.error("Conversion failed: The engine could not read this file.")
            with st.expander("Technical Error Log"):
                st.write("Standard Output:", process.stdout)
                st.write("Error Output:", process.stderr)
                st.write("Files currently in folder:", os.listdir("."))

    except Exception as e:
        st.error(f"System Error: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(in_file): os.remove(in_file)
        if os.path.exists(out_file): os.remove(out_file)
