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
    # 1. We use a completely generic name to stop the "could not be loaded" error
    in_file = "temp_work_file.hwp"
    out_file = "temp_work_file.docx"
    final_name = uploaded_file.name.replace(".hwp", ".docx")
    
    # Save the file
    with open(in_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    bar = st.progress(0)
    status = st.empty()
    status.text("Converting...")

    try:
        # 2. Execute conversion with explicit output directory
        # Using 'cwd=os.getcwd()' ensures the process knows exactly where it is
        process = subprocess.run([
            'soffice', '--headless', '--convert-to', 'docx', in_file
        ], capture_output=True, text=True, timeout=180)

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
            st.error("Conversion failed: The engine could not process this specific file.")
            with st.expander("Technical Error Log"):
                st.code(process.stderr)
                st.write("Current Files:", os.listdir("."))

    except Exception as e:
        st.error(f"System Error: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(in_file): os.remove(in_file)
        if os.path.exists(out_file): os.remove(out_file)
